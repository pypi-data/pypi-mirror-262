"""Compositions of mechanics, controllers, and channels into sensorimotor loops.

:copyright: Copyright 2023-2024 by Matt Laporte.
:license: Apache 2.0. See LICENSE for details.
"""

from collections import OrderedDict
from collections.abc import Callable, Mapping, Sequence
import logging
from typing import Any, Optional, Self, Union, overload

import equinox as eqx
import jax
import jax.numpy as jnp
import jax.random as jr
import jax.tree_util as jtu
from jaxtyping import Array, PRNGKeyArray, PyTree

from feedbax.channel import Channel, ChannelSpec, ChannelState
from feedbax.intervene import AbstractIntervenor
from feedbax._model import AbstractModel, MultiModel
from feedbax.mechanics import Mechanics, MechanicsState
from feedbax.nn import NetworkState
from feedbax._staged import AbstractStagedModel, ModelStage
from feedbax.state import AbstractState, StateBounds
from feedbax.task import AbstractTask
from feedbax._tree import tree_sum_n_features


logger = logging.getLogger(__name__)


class SimpleFeedbackState(AbstractState):
    """Type of state PyTree operated on by [`SimpleFeedback`][feedbax.bodies.SimpleFeedback] instances.

    Attributes:
        mechanics: The state PyTree for a `Mechanics` instance.
        net: The state PyTree for a staged neural network.
        feedback: A PyTree of state PyTrees for each feedback channel.
    """

    mechanics: "MechanicsState"
    net: "NetworkState"
    feedback: PyTree[ChannelState]


def _convert_feedback_spec(
    feedback_spec: Union[
        PyTree[ChannelSpec, "T"], PyTree[Mapping[str, Any], "T"]
    ]
) -> PyTree[ChannelSpec, "T"]:

    if isinstance(feedback_spec, PyTree[ChannelSpec]):
        return feedback_spec

    else:
        feedback_spec_flat, feedback_spec_def = eqx.tree_flatten_one_level(
            feedback_spec
        )
        if all(isinstance(spec, Mapping) for spec in feedback_spec_flat):
            # Specs passed as a PyTree of mappings.
            # Assume it's only one level deep.
            feedback_specs_flat = jax.tree_map(
                lambda spec: ChannelSpec(**spec),
                feedback_spec_flat,
                is_leaf=lambda x: isinstance(x, Mapping),
            )
            return jtu.tree_unflatten(
                feedback_spec_def,
                feedback_specs_flat,
            )
        elif isinstance(feedback_spec, Mapping):
            return ChannelSpec(**feedback_spec)

        else:
            raise ValueError(f"{type(feedback_spec)} is not a valid specification"
                              "PyTree for feedback channels.")


class SimpleFeedback(AbstractStagedModel[SimpleFeedbackState]):
    """Model of one step around a feedback loop between a neural network
    and a mechanical model.

    Attributes:
        net: The neural network that outputs commands for the mechanical model.
        mechanics: The discretized model of plant dynamics.
        feedback_channels: A PyTree of feedback channels which may be delayed
            and noisy.
    """

    net: AbstractModel[NetworkState]
    mechanics: "Mechanics"
    channels: MultiModel[ChannelState]
    _feedback_specs: PyTree[ChannelSpec]
    intervenors: Mapping[str, Sequence[AbstractIntervenor]]

    def __init__(
        self,
        net: AbstractModel[NetworkState],
        mechanics: "Mechanics",
        feedback_spec: Union[
            PyTree[ChannelSpec], PyTree[Mapping[str, Any]]
        ] = ChannelSpec(
            where=lambda mechanics_state: mechanics_state.plant.skeleton,  # type: ignore
        ),
        intervenors: Optional[
            Union[
                Sequence[AbstractIntervenor], Mapping[str, Sequence[AbstractIntervenor]]
            ]
        ] = None,
        *,
        key: Optional[PRNGKeyArray] = None,
    ):
        """
        Arguments:
            net: The neural network that outputs commands for the mechanical model.
            mechanics: The discretized model of plant dynamics.
            feedback_spec: A PyTree of `ChannelSpec` instances,
            intervenors: [Intervenors][feedbax.intervene.AbstractIntervenor] to add
                to the model at construction time.
        """
        self.net = net
        self.mechanics = mechanics
        self.intervenors = self._get_intervenors_dict(intervenors)

        # If `feedback_spec` is given as a `PyTree[Mapping]`, convert to
        # `PyTree[ChannelSpec]`.
        #
        # Allow nesting of mappings to one level, to allow the user to provide
        # (say) a dict of dicts.
        feedback_specs = _convert_feedback_spec(feedback_spec)

        example_mechanics_state = mechanics.init(key=jr.PRNGKey(0))

        def _build_feedback_channel(spec: ChannelSpec):
            return Channel(spec.delay, spec.noise_std, 0.).change_input(
                spec.where(example_mechanics_state)
            )

        self.channels = MultiModel(jax.tree_map(
            lambda spec: _build_feedback_channel(spec),
            feedback_specs,
            is_leaf=lambda x: isinstance(x, ChannelSpec),
        ))
        self._feedback_specs = feedback_specs

    # def update_feedback(
    #     self,
    #     input: "MechanicsState",
    #     state: PyTree[ChannelState, 'T'],
    #     *,
    #     key: Optional[Array] = None
    # ) -> PyTree[ChannelState, 'T']:
    #     """Send current feedback states through channels, and return delayed feedback."""
    #     # TODO: separate keys for the different channels
    #     return jax.tree_map(
    #         lambda channel, spec, state: channel(spec.where(input), state, key=key),
    #         self.feedback_channels,
    #         self._feedback_specs,
    #         state,
    #         is_leaf=lambda x: isinstance(x, Channel),
    #     )

    @property
    def model_spec(self) -> OrderedDict[str, ModelStage[Self, SimpleFeedbackState]]:
        """Specifies the stages of the model in terms of state operations."""
        Stage = ModelStage[Self, SimpleFeedbackState]

        return OrderedDict(
            {
                "update_feedback": Stage(
                    callable=lambda self: self.channels,
                    where_input=lambda input, state: jax.tree_map(
                        lambda spec: spec.where(state.mechanics),
                        self._feedback_specs,
                        is_leaf=lambda x: isinstance(x, ChannelSpec),
                    ),
                    where_state=lambda state: state.feedback,
                ),
                "nn_step": Stage(
                    callable=lambda self: self.net,
                    where_input=lambda input, state: (
                        input,
                        # Get the output state for each feedback channel.
                        jax.tree_map(
                            lambda state: state.output,
                            state.feedback,
                            is_leaf=lambda x: isinstance(x, ChannelState),
                        ),
                    ),
                    where_state=lambda state: state.net,
                ),
                "mechanics_step": Stage(
                    callable=lambda self: self.mechanics,
                    where_input=lambda input, state: state.net.output,
                    where_state=lambda state: state.mechanics,
                ),
            }
        )

    def init(
        self,
        *,
        key: PRNGKeyArray,
    ) -> SimpleFeedbackState:
        """Return a default state for the model."""
        keys = jr.split(key, 3)

        return SimpleFeedbackState(
            mechanics=self.mechanics.init(key=keys[0]),
            # TODO: in case of a wrapped network (i.e. not an `AbstractModel`) a different initialization is needed!
            net=self.net.init(key=keys[1]),  # type: ignore
            feedback=self.channels.init(key=keys[2]),
        )

    @property
    def memory_spec(self) -> PyTree[bool]:
        """Specifies which states should typically be remembered.

        For example, [`ForgetfulIterator`][feedbax.iterate.ForgetfulIterator]
        stores trajectories of states. However it doesn't usually make sense to
        store `states.feedback.queue` for every timestep, because it contains
        info that is already available if `states.mechanics` is stored at every
        timestep. If the feedback delay is 5 steps, `ForgetfulIterator` could
        end up with 5 extra copies of all the parts of `states.mechanics` that
        are part of the feedback. So it may be better not to store
        `states.feedback.queue`.

        This property will be used by `ForgetfulIterator`, but will be ignored
        by [`Iterator`][feedbax.iterate.Iterator], which remembers the full
        state indiscriminately—it's faster, but may use more memory.
        """
        return SimpleFeedbackState(
            mechanics=self.mechanics.memory_spec,
            net=self.net.memory_spec,
            feedback=jax.tree_map(
                lambda channel: channel.memory_spec,
                self.channels.models,
                is_leaf=lambda x: isinstance(x, eqx.Module),
            ),
        )

    @property
    def bounds(self) -> PyTree[StateBounds]:
        """Specifies the bounds of the state."""
        return SimpleFeedbackState(
            mechanics=self.mechanics.bounds,
            net=self.net.bounds,
            feedback=jax.tree_map(
                lambda channel: channel.bounds,
                self.channels.models,
                is_leaf=lambda x: isinstance(x, eqx.Module),
            ),
        )

    @staticmethod
    def get_nn_input_size(
        task: "AbstractTask",
        mechanics: "Mechanics",
        feedback_spec: Union[
            PyTree[ChannelSpec[MechanicsState]], PyTree[Mapping[str, Any]]
        ] = ChannelSpec[MechanicsState](
            where=lambda mechanics_state: mechanics_state.plant.skeleton
        ),
    ) -> int:
        """Determine how many scalar input features the neural network needs.

        This is a static method because its logic (number of network inputs =
        number of task inputs + number of feedback inputs from `mechanics`)
        is related to the structure of `SimpleFeedback`. However, it is
        not an instance method because we want to construct the network
        before we construct `SimpleFeedback`.
        """
        example_mechanics_state = mechanics.init(key=jr.PRNGKey(0))
        example_feedback = jax.tree_map(
            lambda spec: spec.where(example_mechanics_state),
            _convert_feedback_spec(feedback_spec),
            is_leaf=lambda x: isinstance(x, ChannelSpec),
        )
        n_feedback = tree_sum_n_features(example_feedback)
        example_trial_spec = task.get_train_trial(key=jr.PRNGKey(0))
        n_task_inputs = tree_sum_n_features(example_trial_spec.inputs)
        return n_feedback + n_task_inputs

    def state_consistency_update(
        self, state: SimpleFeedbackState
    ) -> SimpleFeedbackState:
        """Returns a corrected initial state for the model.

        1. Update the plant configuration state, given that the user has
        initialized the effector state.
        2. Fill the feedback queues with the initial feedback states. This
        is less problematic than passing all zeros until the delay elapses
        for the first time.
        """
        state = eqx.tree_at(
            lambda state: state.mechanics.plant.skeleton,
            state,
            self.mechanics.plant.skeleton.inverse_kinematics(state.mechanics.effector),
        )

        # If the feedback queues are empty, fill them with the initial feedback values.
        # This is more correct than feeding back all zeros.
        def _fill_feedback_queues(state: SimpleFeedbackState) -> SimpleFeedbackState:
            return eqx.tree_at(
                lambda state: state.feedback,
                state,
                jax.tree_map(
                    lambda channel_state, spec, channel: eqx.tree_at(
                        lambda channel_state: channel_state.queue,
                        channel_state,
                        channel.delay * (spec.where(state.mechanics),),
                    ),
                    state.feedback,
                    self._feedback_specs,
                    self.channels.models,
                    is_leaf=lambda x: isinstance(x, ChannelState),
                ),
            )

        state = _fill_feedback_queues(state)

        # feedback_queues_unfilled = jax.tree_map(lambda x: None in x.queue, state.feedback)

        # state = jax.lax.cond(
        #     any(feedback_queues_unfilled),
        #     _fill_feedback_queues,
        #     lambda state: state,
        #     state,
        # )

        return state
