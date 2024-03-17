import pyro
import pyro.distributions as dist
import torch
import torch.nn as nn
import util
from pyro.infer import SVI, Trace_ELBO
from pyro.optim import Adam
from tqdm import tqdm

def activation(act='relu', **kwargs):
    """Instantiates and returns the specified torch.nn activation object.
    
    Parameters
    ----------
        act : str, default='relu'
            Optional.
            Activation to instantiate.
            Supports 'relu', 'softplus', 'sigmoid', 'softmax' activations.
        kwargs : dict
            Optional.
            Additional arguments needed for the specified activation.

    Raises
    ------
        NotImplementedError
            If the specified activation is not supported.

    Returns
    -------
        activation: torch.nn.*
            Instantiated object corresponding to the specified activation.
    """

    if act == 'relu':
        return nn.ReLU(**kwargs)
    elif act == 'softplus':
        return nn.Softplus(**kwargs)
    elif act == 'sigmoid':
        return nn.Sigmoid(**kwargs)
    elif act == 'softmax':
        return nn.Softmax(dim=-1)
    
    raise NotImplementedError(f'Activation function"{act}" not supported.')

def mlp(layers, bias=True, act='relu', final_act=None, batch_norm=True, affine=True, dropout=0.):
    """Generates linear torch.nn layers with activation, dropout, and optional
    batch normalization.
    
    Parameters
    ----------
        layers : tuple, shape=(n_layers,)
            Sequence of integer values specifying the size of each layer.
        bias : bool, default=True
            Optional.
            Whether or not to learn an additive bias at each layer.
        act : str, default='relu'
            Optional.
            Hidden activation function.
            Supports 'relu', 'softplus', 'sigmoid', and 'softmax' activations.
        final_act : str, default=None
            Optional.
            Final activation function.
            Supports 'softplus', 'relu', 'sigmoid', and 'softmax' activations.
        batch_norm : bool, default=True
            Optional.
            Whether or not to perform final batch normalization.
        affine : bool, default=True
            Optional.
            Whether or not to allow for learnable affine parameters.
        dropout : float, default=0.0
            Optional.
            Probability of random node omission during training.

    Returns
    -------
        mlp : generator
            Iterable object that constructs the specified linear neural network.
    """
    
    n_layers = len(layers) - 1

    for i in range(1, n_layers + 1):
        yield nn.Linear(layers[i - 1], layers[i], bias=bias)
        if i < n_layers - 1:
            yield activation(act)
        else:
            if batch_norm:
                yield nn.BatchNorm1d(layers[i], affine=affine)
            if final_act:
                yield activation(final_act)
            yield nn.Dropout(dropout)

class MLP(nn.Module):
    """TODO

    Parameters
    ----------
        layers : tuple, shape=(n_layers,)
            Sequence of integer values specifying the size of each layer.
        bias : bool, default=True
            Optional.
            Whether or not to learn an additive bias at each layer.
        act : str, default='relu'
            Optional.
            Hidden activation function.
            Supports 'softplus', 'relu', 'sigmoid', and 'softmax' activations.
        final_act : str, default=None
            Optional.
            Final activation function.
            Supports 'softplus', 'relu', 'sigmoid', and 'softmax' activations.
        batch_norm : bool, default=True
            Optional.
            Whether or not to perform final batch normalization.
        affine : bool, default=True
            Optional.
            Whether or not to allow for learnable affine parameters.
        dropout : float, default=0.0
            Optional.
            Probability of random node omission during training.
        
    Attributes
    ----------
        net : torch.nn.Sequential
            TODO
    """

    def __init__(self, layers, bias=True, act='relu', final_act=None, batch_norm=True, affine=True, dropout=0.):
        super().__init__()

        self.net = nn.Sequential(*list(mlp(layers, bias, act, final_act, batch_norm, affine, dropout)))
    
    def forward(self, x):
        """TODO
        
        Parameters
        ----------
            x : torch.Tensor, shape=(batch_size, input_dim)
                TODO

        Returns
        -------
            y : torch.Tensor, shape=(batch_size, output_dim)
                TODO
        """

        y = self.net(x)

        return y

class Encoder(nn.Module):
    """TODO

    Parameters
    ----------
        layers : tuple, shape=(n_layers)
            TODO
        
    Attributes
    ----------
        encoding_net : Class[torch.nn.Module]
            TODO
        loc_net : Class[torch.nn.Module]
            TODO
        scale_net : Class[torch.nn.Module]
            TODO
    """
    
    def __init__(self, *layers):
        super().__init__()

        encoding_layers = layers[:-1]
        self.encoding_net = MLP(encoding_layers, final_act='softplus', batch_norm=False, dropout=.2)

        latent_layers = layers[-2:]
        self.loc_net, self.scale_net = MLP(latent_layers), MLP(latent_layers)

    def forward(self, x):
        """TODO
        
        Parameters
        ----------
            x : torch.Tensor, shape=(batch_size, input_dim)
                TODO
        
        Returns
        -------
            z_loc : torch.Tensor, shape=(batch_size, latent_dim)
                TODO
            z_scale : torch.Tensor, shape=(batch_size, latent_dim)
                TODO
        """
        
        y = self.encoding_net(x)
        z_loc = self.loc_net(y)
        z_scale = (.5*self.scale_net(y)).exp()

        return z_loc, z_scale
    
class Decoder(nn.Module):
    """TODO
    
    Parameters
    ----------
        layers : tuple, shape=(n_layers)
            TODO
        
    Attributes
    ----------
        net : Class[torch.nn.Module]
            TODO
    """

    def __init__(self, *layers):
        super().__init__()

        self.net = MLP(layers)

    def forward(self, z):
        """TODO
        
        Parameters
        ----------
            z : torch.Tensor, shape=(batch_size, latent_dim)
                TODO

        Returns
        -------
            x : torch.Tensor, shape=(batch_size, output_dim)
                TODO
        """

        x = self.net(z)

        return x

class VAE(nn.Module):
    """TODO
    
    Parameters
    ----------
        layers : tuple, shape=(n_layers)
            TODO
        scale : float, default=1.0
            Optional.
            TODO
        batch_size : int, default=None
            Optional.
            TODO
        seed : int, default=9
            Optional.
            TODO
        
    Attributes
    ----------
        encoder : Class[torch.nn.Module]
            TODO
        decoder : Class[torch.nn.Module]
            TODO
        training_log_ : list, shape=(n_steps,)
            TODO
        validation_log_ : list, shape=(n_steps,)
            TODO
    """

    def __init__(self, *layers, scale=.1, batch_size=None, seed=9):
        super().__init__()
        pyro.clear_param_store()

        if seed is not None:
            util.set_seed(seed)

        self.layers = layers
        self.scale = scale
        self.batch_size = batch_size

        self.encoder = Encoder(*layers)
        self.decoder = Decoder(*layers[::-1])
        self.training_log_ = []
        self.validation_log_ = []
        self.patience_log_ = []

    def _disp(self, idx, desc='VAE'):
        """TODO
        
        Parameters
        ----------
            idx : int
                TODO
            desc : str, default='VAE'

        Returns
        -------
            disp : str
                TODO
        """

        scores = self.training_log_[idx], self.validation_log_[idx], sum(self.patience_log_[idx])
        disp = f'{desc} | step {idx} | training loss: {scores[0]} | validation loss: {scores[1]} | patience: {scores[2]}'

        return disp
    
    def _build(self, learning_rate):
        """TODO
        
        Parameters
        ----------
            learning_rate : float
                TODO

        Returns
        -------
            elbo : TODO
                TODO
            svi : TODO
                TODO
        """

        optim = Adam({'lr': learning_rate})
        elbo = Trace_ELBO(max_iarange_nesting=4)
        svi = SVI(self._model, self._guide, optim, elbo)

        return elbo, svi

    def _patience(self, idx, window):
        """TODO
        
        Parameters
        ----------
            idx : int
                TODO
            window : int
                TODO

        Returns
        -------
            patience : bool
                TODO
        """

        if idx%window == 0 and idx > 2*window:
            return sum(self.validation_log_[-window:]) >= sum(self.validation_log_[-2*window:-window])
        return False
    
    def _model(self, x):
        """TODO
        
        Parameters
        ----------
            x : torch.Tensor, shape=(n_samples, input_dim)
                TODO

        Returns
        -------
            None
        """
        
        pyro.module('decoder', self.decoder)

        with pyro.plate('data', x.shape[0], self.batch_size) as idx:
            z_loc = x[idx].new_zeros((x[idx].shape[0], self.layers[-1]))
            z_scale = x[idx].new_ones((x[idx].shape[0], self.layers[-1]))
            z = pyro.sample('latent', dist.Normal(z_loc, z_scale).to_event(1))
            x_loc = self.decoder(z)
            x_scale = self.scale*torch.ones_like(x_loc)
            pyro.sample('obs', dist.Normal(x_loc, x_scale).to_event(1), obs=x[idx])

    def _guide(self, x):
        """TODO
        
        Parameters
        ----------
            x : torch.Tensor, shape=(n_samples, input_dim)
                TODO

        Returns
        -------
            None
        """

        pyro.module('encoder', self.encoder)

        with pyro.plate('data', x.shape[0], self.batch_size) as idx:
            z_loc, z_scale = self.encoder(x[idx])
            pyro.sample('latent', dist.Normal(z_loc, z_scale).to_event(1))

    def fit(self, X, n_steps=1000, learning_rate=1e-2, patience=10, window=5, val_split=.2, desc='VAE', verbose=1, info_rate=10):
        """TODO
        
        Parameters
        ----------
            X : torch.Tensor, shape=(n_samples, input_dim)
                Dataset with which to train the networks.
            n_steps : int, default=1000
                Optional.
                Number of steps to train the networks for.
            learning_rate : float, default=1e-2
                Optional.
                Step size for gradient descent during training.
            patience : int, default=10
                Optional.
                TODO
            window : int, default=5
                Optional.
                TODO
            val_split : float, default=0.2
                Optional.
                TODO
            desc : str, default='VAE'
                Optional.
                Description displayed with information reported during training.
            verbose : int, default=1
                Optional.
                Level of verbosity of information reported during training.
                Supports 0, 1, and 2.
            info_rate : int, default=10
                Optional.
                TODO

        Returns
        -------
            self
                I return therefore I am.
        """

        idx = torch.randperm(X.shape[0])
        split_idx = int(val_split*X.shape[0])
        X_train, X_val = X[idx[split_idx:]], X[idx[:split_idx]]
        elbo, svi = self._build(learning_rate)
        
        for i in tqdm(range(n_steps), desc=desc) if verbose == 1 else range(n_steps):
            training_loss = svi.step(X_train)

            with torch.no_grad():
                self.training_log_.append(training_loss)
                self.validation_log_.append(elbo.loss(self._model, self._guide, X_val))
                self.patience_log_.append(self._patience(i, window))

                if verbose == 2 and i%info_rate == 0:
                    print(self._disp(i, desc))

                if sum(self.patience_log_) >= patience:
                    break

        return self
    
    def transform(self, X):
        """TODO
        
        Parameters
        ----------
            X : torch.Tensor, shape=(n_samples, input_dim)
                Dataset with which the networks were trained.
            
        Returns
        -------
            Z : torch.Tensor, shape=(n_samples, latent_dim)
                Dataset sampled from the latent space encoded with X
        """

        Z_loc, Z_scale = self.encoder(X)
        Z = dist.Normal(Z_loc, Z_scale).sample()

        return Z
