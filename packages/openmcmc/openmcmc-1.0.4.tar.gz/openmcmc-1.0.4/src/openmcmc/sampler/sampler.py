# SPDX-FileCopyrightText: 2024 Shell Global Solutions International B.V. All Rights Reserved.
#
# SPDX-License-Identifier: Apache-2.0

"""Collection of functions defining various MCMC samplers.

MCMCSampler is a superclass for all MCMC sampler types. This file contains several conjugate MCMC sampling algorithms,
which can be used for specific distribution combinations, and inherit directly from MCMCSampler.

metropolis_hastings.py contains another set of algorithms, all of Metropolis-Hastings type, where a parameter proposal
followed by an accept/reject step.

reversible_jump.py contains a generic implementation of the reversible jump algorithm.

"""

from abc import ABC, abstractmethod
from copy import deepcopy
from dataclasses import dataclass
from typing import Union

import numpy as np
from scipy import sparse
from scipy.stats import gamma, norm

from openmcmc import gmrf
from openmcmc.distribution.location_scale import Normal
from openmcmc.model import Model
from openmcmc.parameter import (
    Identity,
    MixtureParameterMatrix,
    MixtureParameterVector,
    ScaledMatrix,
)


@dataclass
class MCMCSampler(ABC):
    """Abstract base class for openMCMC sampling algorithms for a model parameter.

    Attributes:
        param (str): label of the parameter to be sampled.
        model (Model): sub-model of overall model, containing only distributions with some dependence on self.param.
        max_variable_size (Union[int, tuple]): (if required) maximum size for the variable. Only relevant in cases
            (e.g. RJMCMC) where variable dimension changes as a result of MCMC proposals.

    """

    param: str
    model: Model
    max_variable_size: Union[int, tuple, None] = None

    def __post_init__(self):
        """Extract the sub-model of distributions with some dependence on self.param."""
        self.model = self.model.conditional(self.param)

    @abstractmethod
    def sample(self, current_state: dict) -> dict:
        """Generate the next sample in the chain.

        Args:
            current_state (dict): dictionary containing current parameter values.

        Returns:
            (dict): state with the value of self.param updated to a new sample.

        """

    def init_store(self, current_state: dict, store: dict, n_iterations: int) -> dict:
        """Initialise the field in the MCMC storage dictionary for self.param.

        Args:
            current_state (dict): dictionary containing current parameter values.
            store (dict): dictionary to store all samples generated by the MCMC algorithm.
            n_iterations (int): total number of MCMC iterations to be run.

        Returns:
            (dict): storage dictionary updated with field for self.param.

        """
        if self.max_variable_size is None:
            store[self.param] = np.full(shape=(np.size(current_state[self.param]), n_iterations), fill_value=np.nan)
        elif isinstance(self.max_variable_size, tuple):
            store[self.param] = np.full(shape=self.max_variable_size + (n_iterations,), fill_value=np.nan)
        else:
            store[self.param] = np.full(shape=(self.max_variable_size, n_iterations), fill_value=np.nan)
        return store

    def store(self, current_state: dict, store: dict, iteration: int) -> dict:
        """Store the current state of the sampled variable in the MCMC storage dictionary.

        If self.parameter is not initialised in the MCMC state, then the function generates a random sample from the
        corresponding distribution in model.

        Args:
            current_state (dict): dictionary with current parameter values.
            store (dict): storage dictionary for MCMC samples.
            iteration (int): current MCMC iteration index.

        Returns:
            dict: storage dictionary updated with values from current iteration.

        """
        current_param = current_state[self.param]

        if self.max_variable_size is None:
            store[self.param][:, [iteration]] = current_param
        elif isinstance(self.max_variable_size, tuple):
            index_list = []
            for dim in range(current_param.ndim):
                index_list.append(np.arange(current_param.shape[dim], dtype=int))
            index_list.append(np.array([iteration]))

            store[self.param][np.ix_(*index_list)] = current_param.reshape(current_param.shape + (1,))
        else:
            store[self.param][range(current_param.size), [iteration]] = current_param.flatten()

        return store


@dataclass
class NormalNormal(MCMCSampler):
    """Normal-Normal conditional sampling (exploiting conjugacy).

    Sample from f(x|{b_k}) ~= [prod_k f(y_k|x)]f(x) where the components have the following form:
        - Likelihoods: f(y_k|x) ~ N(y_k | d_k + A_k*a, W_k^{-1})
        - Prior: f(x) ~ N(x |m, P^{-1})
    The following features are assumed:
        - There can be multiple likelihood/response distributions, but there is only one prior distribution.
        - The mean of each of the response distributions must have a linear dependence on self.param.
        - The prior Gaussian can be truncated (as long as the truncation points are constant), but the response
            Gaussians cannot.

    If the prior Gaussian is truncated (i.e. it has specified domain limits), then those same domain limits will be
    used when generating the conditional sample.

    Attributes:
        _is_response (dict): dictionary containing boolean indicators for whether self.param is the response of the
            distribution. If self._is_response[key] is True, then self.param is the response of the distribution.

    """

    def __post_init__(self):
        """Identify and extract the sub-model with a dependence on self.param.

        Also identify whether self.param is the response for each of the pair of Gaussian distributions.

        """
        super().__post_init__()
        self._is_response = {}
        for key in self.model.keys():
            self._is_response[key] = key == self.param

    def sample(self, current_state: dict) -> dict:
        """Generate a sample from a Gaussian-Gaussian conditional distribution.

        For a Gaussian-Gaussian conditional distribution, the parameters are as follows:
            Conditional precision:
                Q = P + sum_k [A_k'*W_k*A_k]
            Conditional mean:
                b = P*m + sum_k [A_k'*W_k*(y_k - d_k)]
                mu = Q^{-1} * b
        Where the parameters are as defined in the class docstring.

        If the supplied response parameter has a second dimension, these are interpreted as repeated draws from the same
        distribution, and are thus summed. The multiplication of the precision matrix by num_replicates is handled by
        the grad_log_p() function of the corresponding distribution.

        Args:
            current_state (dict): dictionary containing the current sampler state.

        Returns:
            (dict): state with updated value for self.param.

        """
        n_param = current_state[self.param].shape[0]
        Q = sparse.csc_matrix((n_param, n_param))
        b = np.zeros(shape=(n_param, 1))
        for key, dist in self.model.items():
            Q_rsp = dist.precision.predictor(current_state)
            if self._is_response[key]:
                Q += Q_rsp
                b += Q_rsp @ dist.mean.predictor(current_state)
            else:
                _, Q_dist = dist.grad_log_p(current_state, self.param)
                Q += Q_dist
                if isinstance(dist.mean, Identity):
                    b += Q_rsp @ np.sum(current_state[key], axis=1, keepdims=True)
                else:
                    predictor_exclude = dist.mean.predictor_conditional(current_state, term_to_exclude=self.param)
                    A = current_state[dist.mean.form[self.param]]
                    b += A.T @ Q_rsp @ (current_state[key] - predictor_exclude)

        dist_param = self.model[self.param]

        if dist_param.domain_response_lower is None and dist_param.domain_response_upper is None:
            current_state[self.param] = gmrf.sample_normal_canonical(b, Q)
        else:
            current_state[self.param] = gmrf.gibbs_canonical_truncated_normal(
                b,
                Q,
                x=current_state[self.param],
                lower=dist_param.domain_response_lower,
                upper=dist_param.domain_response_upper,
            )

        return current_state


@dataclass
class NormalGamma(MCMCSampler):
    """Normal-gamma conditional sampling (exploiting conjugacy).

    Assumes that self.param is the precision parameter for a Gaussian response distribution, and that it has a gamma
    prior distribution.

    Allows for the possibility that a single Gaussian response distribution might be associated with a number of
    different precision parameters, through use of a MixtureParameterMatrix precision parameters. These parameters
    are sampled in a loop within the sample function.

    This class samples from f(lam|y, a, b) ~ prod_k [f(y_k|lam)]f(lam|a,b) where
        - Likelihoods: f(y_k|lam) ~ N(mu_k, 1/lam)
        - Prior: f(lam|a, b) ~ G(a, b)
    Note that it is also possible to use a more complex (e.g. dense) precision matrix scaled by a single precision
    parameter, this does not fundamentally change the approach.

    Attributes:
        param (str): label of parameter name to be sampled
        normal_param (str): label of corresponding normal parameter
        model (Model): conditional model with distributions related to param only

    """

    def __post_init__(self):
        """Complete initialization of sampler.

        Identifies the gamma distribution and its conjugate normal distribution, and attaches copies to the sampler
        object.

        """
        super().__post_init__()

        nrm_prm = list(self.model.keys())
        nrm_prm.remove(self.param)
        self.normal_param = nrm_prm[0]

        precision = self.model[self.normal_param].precision

        if not isinstance(precision, (Identity, ScaledMatrix, MixtureParameterMatrix)):
            raise TypeError("precision must be either Identity, ScaledMatrix or MixtureParameterMatrix")

    def sample(self, current_state: dict) -> dict:
        """Generate a sample from a (series of) Gaussian-Gamma conditional distribution.

        The conditional distribution for an individual parameter is:
            G(a*, b*)
        where:
            a* = a_0 + n/2
            b* = b_0 + (y - y_hat)' * P * (y - y_hat)
        where n = [dimension of normal response], P = [un-scaled precision matrix].

        It is assumed that the precision parameter of the Gaussian distribution has a predictor_unscaled() method,
        which can be used to identify the subset of the full precision matrix which is dependent on the parameter being
        sampled: this is returned un-scaled by the precision parameter.

        Args:
            current_state (dict): dictionary containing the current sampler state.

        Returns:
            (dict): state with updated value for self.param.

        """
        precision = self.model[self.normal_param].precision
        mean = self.model[self.normal_param].mean
        y = current_state[self.model[self.normal_param].response]
        residual = y - mean.predictor(current_state)

        a = deepcopy(self.model[self.param].shape.predictor(current_state))
        b = deepcopy(self.model[self.param].rate.predictor(current_state))

        for k in range(current_state[self.param].shape[0]):
            precision_unscaled = precision.precision_unscaled(current_state, k)
            a[k] += np.sum(precision_unscaled.diagonal() > 0) / 2
            b[k] += (residual.T @ precision_unscaled @ residual).item() / 2
        no_warning_b = np.where(b == 0, np.inf, b)
        no_warning_scale = np.where(b == 0, np.inf, 1 / no_warning_b)
        current_state[self.param] = gamma.rvs(a, scale=no_warning_scale).reshape(current_state[self.param].shape)
        return current_state


@dataclass
class MixtureAllocation(MCMCSampler):
    """Conditional conjugate sampling of the allocation in a mixture distribution. Can be used with any kind of mixture distribution.

    This class samples from:
        f(z|y, lam, tht) ~ f(y|z, lam)f(z|tht)
    where:
        - Likelihood: f(y|z, lam); Gaussian distribution, with different characteristics depending on z.
        - Prior: f(z|tht); categorical distribution, with prior allocation probabilities tht.

    Attributes:
        response_param (str): name of the response parameter associated with the allocation parameter.

    """

    response_param: Union[str, None] = None

    def __post_init__(self):
        """Subset only model elements relevant for this sampler."""
        self.model = Model([self.model[self.param], self.model[self.response_param]])

        if not isinstance(self.model[self.response_param], Normal):
            raise TypeError("Mixture model currently only implemented for Normal case")

        if not isinstance(self.model[self.response_param].mean, MixtureParameterVector):
            raise TypeError("Mean must be of type MixtureParameterVector")

        if not isinstance(self.model[self.response_param].precision, MixtureParameterMatrix):
            raise TypeError("Mean must be of type MixtureParameterMatrix")

    def sample(self, current_state: dict) -> dict:
        """Generate sample of a parameter allocation given current state of the sampler.

        Computes the conditional allocation probability for each element of the response to each component of the
        mixture, then samples an allocation based on the probabilities.

        The conditional distribution is:
            Cat([gam_1, gam_2,..., gam_m])
        where:
            gam_k = f(y|z_k, lam) * tht_k / W
            W = sum_k [f(y|z_k, lam) * tht_k / Z]

        Args:
            current_state (dict): dictionary containing the current sampler state.

        Returns:
            (dict): state with updated value for self.param.

        """
        allocation_prior = self.model[self.param].prob.predictor(current_state)
        n_response = current_state[self.response_param].shape[0]
        component_mean = current_state[self.model[self.response_param].mean.param]
        component_precision = current_state[self.model[self.response_param].precision.param]

        allocation_prob = np.empty((n_response, allocation_prior.shape[1]))
        for k in range(allocation_prior.shape[1]):
            allocation_prob[:, [k]] = allocation_prior[:, [k]] * norm.pdf(
                current_state[self.response_param], loc=component_mean[k], scale=1 / np.sqrt(component_precision[k])
            )

        allocation_prob = allocation_prob / np.sum(allocation_prob, axis=1).reshape((allocation_prob.shape[0], 1))
        U = np.random.rand(n_response, 1)
        current_state[self.param] = np.atleast_2d(np.sum(U > np.cumsum(allocation_prob, axis=1), axis=1)).T

        return current_state
