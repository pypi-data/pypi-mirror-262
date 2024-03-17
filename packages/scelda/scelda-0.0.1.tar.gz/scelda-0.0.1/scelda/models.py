import numpy as np
import torch
import util
from nets import VAE
from scipy.cluster.vq import kmeans, vq
from scipy.spatial.distance import cdist
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.metrics import silhouette_score
from tqdm import tqdm

class SLDA(BaseEstimator, TransformerMixin):
    """TODO
    
    Parameters
    ----------
        n_topics : int
            TODO
        n_docs : int, default=150
            Optional.
            TODO
        vocab_size : int, default=25
            Optional.
            TODO
        vocab_steps : int, default=10
            Optional.
            TODO
        sigma : float, default=0.1
            Optional.
            TODO
        alpha : float, default=None
            Optional.
            TODO
        beta : float, default=None
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
        corpus_ : numpy.ndarray, shape=(n_samples, 6)
            TODO
        doc_locs_ : numpy.ndarray, shape=(n_docs, 3)
            TODO
        doc_topic_counts_ : numpy.ndarray, shape=(n_docs, n_topics)
            TODO
        topic_word_counts_ : numpy.ndarray, shape=(n_topics, vocab_size)
            TODO
        likelihood_log_ : list, shape=(n_steps,)
            TODO
    """

    def __init__(self, n_topics, n_docs=150, vocab_size=25, vocab_steps=10, sigma=.1, alpha=None, beta=None, batch_size=None, seed=9):
        super().__init__()

        if seed is not None:
            util.set_seed(seed)

        self.n_topics = n_topics
        self.n_docs = n_docs
        self.vocab_size = vocab_size
        self.vocab_steps = vocab_steps
        self.sigma = sigma
        self.alpha = 1/n_docs if alpha is None else alpha
        self.beta = 1/n_topics if beta is None else beta
        self.batch_size = batch_size

        self.corpus_ = None
        self.doc_locs_ = None
        self.doc_topic_counts_ = None
        self.topic_word_counts_ = None
        self.likelihood_log_ = []
        self.silhouette_log_ = []
        self.patience_log_ = []

    def _disp(self, idx, desc='SLDA'):
        """TODO
        
        Parameters
        ----------
            idx : int
                TODO
            desc : str, default='SLDA'
                TODO

        Returns
        -------
            disp : str
                TODO
        """

        scores = self.likelihood_log_[idx], self.patience_log_[idx]
        disp = f'{desc} | step {idx} | likelihood: {scores[0]} | patience: {scores[1]}'

        return disp

    def _featurize(self, locs, markers):
        """TODO
        
        Parameters
        ----------
            locs : numpy.ndarray, shape=(n_samples, 3)
                TODO
            markers : numpy.ndarray, shape=(n_samples, n_features)
                TODO

        Returns
        -------
            features : numpy.ndarray, shape=(n_samples, n_features)
                TODO
        """
        
        n_imgs = np.unique(locs[:, 0]).shape[0]
        features = []

        for i in range(n_imgs):
            idx = locs[:, 0] == i
            dists = cdist(locs[idx, 1:], locs[idx, 1:])
            weights = np.exp(-(dists/self.sigma)**2)
            features.append(weights.T@markers[idx])

        features = np.vstack(features)

        return features

    def _shuffle(self, words):
        """TODO
        
        Parameters
        ----------
            words : numpy.ndarray, shape=(n_samples,)
                TODO

        Returns
        -------
            docs : numpy.ndarray, shape=(n_samples,)
                TODO
            topics : numpy.ndarray, shape=(n_samples,)
                TODO
        """
        
        docs = np.random.choice(self.n_docs, (words.shape[0], 1))
        topics = np.random.choice(self.n_topics, (words.shape[0], 1))
        doc_range, topic_range = np.arange(self.n_docs), np.arange(self.n_topics)
        self.doc_topic_counts_ = (docs == doc_range).T@np.eye(self.n_topics)[topics.T[0]]
        self.topic_word_counts_ = (topics == topic_range).T@np.eye(self.vocab_size)[words]

        return docs, topics
    
    def _build(self, data):
        """TODO
        
        Parameters
        ----------
            data : numpy.ndarray, shape=(n_samples, n_features)
                TODO

        Returns
        -------
            corpus_ : numpy.ndarray, shape=(n_samples, 6)
                TODO
        """

        locs, markers = data[:, :3], data[:, 3:]
        self.n_docs = np.unique(locs[:, 0]).shape[0]*self.n_docs
        doc_idx = np.random.permutation(data.shape[0])[:self.n_docs]
        self.doc_locs_ = locs[doc_idx]
        features = self._featurize(locs, markers)
        codebook, _ = kmeans(features, self.vocab_size, self.vocab_steps)
        words, _ = vq(features, codebook)
        docs, topics = self._shuffle(words)
        self.corpus_ = np.hstack([locs, words[None].T, docs, topics])

        if self.batch_size is None:
            self.batch_size = self.corpus_.shape[0]

        return self.corpus_
    
    def _patience(self, idx, window):
        """TODO
        
        Parameters
        ----------
            window : int
                TODO

        Returns
        -------
            patience : bool
                TODO
        """

        if idx%window == 0 and idx > 2*window:
            return sum(self.likelihood_log_[-window:]) <= sum(self.likelihood_log_[-2*window:-window])
        return False
    
    def _sample_doc(self, loc, topic, return_likelihood=False):
        """TODO
        
        Parameters
        ----------
            loc : numpy.ndarray, shape=(3,)
                TODO
            topic : int
                TODO
            return_likelihood : bool, default=False
                Optional.
                TODO

        Returns
        -------
            doc : int
                TODO
            likelihood : float
                TODO
        """

        mask = (self.doc_locs_[:, 0] == loc[0]).astype(np.int32)
        doc_probs = mask*self.sigma**2/(((loc[1:] - self.doc_locs_[:, 1:])**2).sum(-1) + 1e-100)
        topic_probs = self.doc_topic_counts_[:, topic] + self.alpha
        topic_probs /= (self.doc_topic_counts_ + self.alpha).sum(-1)
        probs = doc_probs*topic_probs/(doc_probs*topic_probs).sum()
        doc = np.random.choice(self.n_docs, p=probs)
        
        if return_likelihood:
            return doc, probs[doc]
        
        return doc
    
    def _sample_topic(self, word, doc, return_likelihood=False, maximize=False):
        """TODO
        
        Parameters
        ----------
            word : int
                TODO
            doc : int
                TODO
            return_likelihood : bool, default=False
                Optional.
                TODO
            maximize : bool, default=False
                Optional.
                TODO

        Returns
        -------
            topic : int
                TODO
            likelihood : float
                TODO
        """

        topic_probs = self.doc_topic_counts_[doc] + self.alpha
        topic_probs /= (self.doc_topic_counts_[doc] + self.alpha).sum()
        word_probs = self.topic_word_counts_[:, word] + self.beta
        word_probs /= (self.topic_word_counts_ + self.beta).sum(-1)
        probs = topic_probs*word_probs/(topic_probs*word_probs).sum()
        topic = np.argmax(probs) if maximize else np.random.choice(self.n_topics, p=probs)

        if return_likelihood:
            return topic, probs[topic]
        
        return topic
    
    def _sample(self, loc, word, old_doc, old_topic, return_likelihood=False, maximize=False):
        """TODO
        
        Parameters
        ----------
            loc : numpy.ndarray, shape=(3,)
                TODO
            word : int
                TODO
            old_doc : int
                TODO
            old_topic : int
                TODO
            return_likelihood : bool, default=False
                Optional.
                TODO
            maximize : bool, default=False
                Optional.
                TODO

        Returns
        -------
            new_doc : int
                TODO
            new_topic : int
                TODO
            likelihood : float
                TODO
        """
        
        new_doc, doc_likelihood = self._sample_doc(loc, old_topic, return_likelihood)
        new_topic, topic_likelihood = self._sample_topic(word, old_doc, return_likelihood, maximize)
        
        if return_likelihood:
            return new_doc, new_topic, doc_likelihood + topic_likelihood

        return new_doc, new_topic
    
    def _decrement(self, word, doc, topic):
        """TODO
        
        Parameters
        ----------
            word : int
                TODO
            doc : int
                TODO
            topic : int
                TODO

        Returns
        -------
            doc_topic_counts_ : numpy.ndarray, shape=(n_docs, n_topics)
                TODO
            topic_word_counts_ : numpy.ndarray, shape=(n_topics, vocab_size)
                TODO
        """

        self.doc_topic_counts_[doc, topic] -= 1
        self.topic_word_counts_[topic, word] -= 1

        return self.doc_topic_counts_, self.topic_word_counts_
    
    def _increment(self, word, doc, topic):
        """TODO
        
        Parameters
        ----------
            word : int
                TODO
            doc : int
                TODO
            topic : int
                TODO

        Returns
        -------
            doc_topic_counts_ : numpy.ndarray, shape=(n_docs, n_topics)
                TODO
            topic_word_counts_ : numpy.ndarray, shape=(n_topics, vocab_size)
                TODO
        """

        self.doc_topic_counts_[doc, topic] += 1
        self.topic_word_counts_[topic, word] += 1

        return self.doc_topic_counts_, self.topic_word_counts_
    
    def _step(self, maximize=False):
        """TODO
        
        Parameters
        ----------
            maximize : bool, default=False
                Optional.
                TODO

        Returns
        -------
            likelihood_avg : float
                TODO
        """

        likelihood_sum = 0

        for i in range(self.corpus_.shape[0]):
            loc, (word, old_doc, old_topic) = self.corpus_[i, :3], self.corpus_[i, 3:].astype(np.int32)
            self._decrement(word, old_doc, old_topic)
            new_doc, new_topic, likelihood = self._sample(loc, word, old_doc, old_topic, return_likelihood=True, maximize=maximize)
            self._increment(word, new_doc, new_topic)
            self.corpus_[i, -2:] = new_doc, new_topic
            likelihood_sum += likelihood

        return likelihood_sum
    
    def fit(self, X, n_steps=500, patience=10, window=1, desc='SLDA', verbose=1, info_rate=10):
        """TODO
        
        Parameters
        ----------
            X : numpy.ndarray, shape=(n_samples, n_features)
                TODO
            n_steps : int, default=1000
                Optional.
                TODO
            patience : int, default=10
                Optional.
                TODO
            window : int, default=1
                Optional.
                TODO
            desc : str, default='SLDA'
                Optional.
                TODO
            verbose : int, default=1
                Optional.
                TODO
            info_rate : int, default=10
                Optional.
                TODO

        Returns
        -------
            self
                I return therefore I am.
        """

        self._build(X)

        for i in tqdm(range(n_steps), desc=desc) if verbose == 1 else range(n_steps):
            likelihood = self._step()
            self.likelihood_log_.append(likelihood)
            self.silhouette_log_.append(silhouette_score(X, self.transform(X)))
            self.patience_log_.append(self._patience(i, window))

            if verbose == 2 and i%info_rate == 0:
                print(self._disp(i, desc))
           
            if sum(self.patience_log_) >= patience:
                break

        return self
    
    def transform(self, _=None):
        """TODO
        
        Parameters
        ----------
            None

        Returns
        -------
            topics : numpy.ndarray, shape=(n_samples,)
                TODO
        """
        
        topics = np.zeros(self.corpus_.shape[0], dtype=np.int32)

        for i in range(self.corpus_.shape[0]):
            word, doc = self.corpus_[i, 3:5].astype(np.int32)
            topics[i] = self._sample_topic(word, doc)

        return topics

class sceLDA(BaseEstimator, TransformerMixin):
    """TODO
    
    Parameters
    ----------
        n_topics : int
            TODO
        hidden_dim : tuple, shape=(n_hidden,), default=(100, 50)
            Optional.
            TODO
        latent_dim : int, default=25
            Optional.
            TODO
        scale : float, default=0.1
            Optional.
            TODO
        batch_size : int, default=None
            Optional.
            TODO
        n_docs : int, default=150
            Optional.
            TODO
        vocab_size : int, default=25
            Optional.
            TODO
        vocab_steps : int, default=10
            Optional.
            TODO
        sigma : float, default=0.1
            Optional.
            TODO
        alpha : float, default=None
            Optional.
            TODO
        beta : float, default=None
            Optional.
            TODO

    Attributes
    ----------
        vae : Class[torch.nn.Module]
            TODO
        slda : Class[sklearn.base.BaseEstimator, sklearn.base.TransformerMixin]
            TODO
    """

    def __init__(self, n_topics, hidden_dim=(100, 50), latent_dim=25, scale=.1, batch_size=None, n_docs=150, vocab_size=25, vocab_steps=10, sigma=.1, alpha=None, beta=None):
        super().__init__()
        
        self.n_topics = n_topics
        self.hidden_dim = hidden_dim
        self.latent_dim = latent_dim
        self.scale = scale
        self.batch_size = batch_size
        self.n_docs = n_docs
        self.vocab_size = vocab_size
        self.vocab_steps = vocab_steps
        self.sigma = sigma
        self.alpha = alpha
        self.beta = beta

        self.vae = None
        self.slda = None

    def _build(self, input_dim):
        """TODO
        
        Parameters
        ----------
            input_dim : int
                TODO
        
        Returns
        -------
            vae : Class[torch.nn.Module]
                TODO
            slda : Class[sklearn.base.BaseEstimator, sklearn.base.TransformerMixin]
                TODO
        """

        if self.vae is None:
            layers = (input_dim,) + self.hidden_dim + (self.latent_dim,)
            self.vae = VAE(*layers, scale=self.scale, batch_size=self.batch_size)

        if self.slda is None:
            self.slda = SLDA(self.n_topics, self.n_docs, self.vocab_size, self.vocab_steps, self.sigma, self.alpha, self.beta)

        return self.vae, self.slda
    
    def tune(self, param_grid, threshold=.99):
        """TODO
        
        Parameters
        ----------
            param_grid : dict
                TODO
            threshold : float, default=0.99
                Optional.
                TODO

        Returns
        -------
            self
                I return therefore I am.
        """


    
    def fit(self, X, n_vae_steps=1000, learning_rate=1e-2, vae_patience=10, vae_window=5, n_slda_steps=500, slda_patience=20, slda_window=5, verbose=1, info_rate=10):
        """TODO
        
        Parameters
        ----------
            X : torch.tensor, shape=(n_samples, n_features)
                TODO
            n_vae_steps : int, default=1000
                Optional.
                TODO
            learning_rate : float, default=1e-2
                Optional.
                TODO
            vae_patience : int, default=10
                Optional.
                TODO
            vae_window : int, default=5
                Optional.
                TODO
            n_slda_steps : int, default=500
                Optional.
                TODO
            slda_patience : int, default=10
                Optional.
                TODO
            slda_window : int, default=5
                Optional.
                TODO
            verbose : int, default=1
                Optional.
                TODO
            info_rate : int, default=10
                Optional.
                TODO

        Returns
        -------
            self
                I return therefore I am.
        """

        if not torch.is_tensor(X):
            X = torch.tensor(X, dtype=torch.float32)

        self._build(X.shape[1] - 3)
        locs, features = X[:, :3], X[:, 3:]
        self.vae.fit(features, n_vae_steps, learning_rate, vae_patience, vae_window, verbose=verbose, info_rate=info_rate)
        Z = torch.hstack([locs, self.vae.transform(features)]).detach().numpy()
        self.slda.fit(Z, n_slda_steps, slda_patience, slda_window, verbose=verbose, info_rate=info_rate)

        return self
    
    def transform(self, X):
        """TODO
        
        Parameters
        ----------
            X : torch.tensor, shape=(n_samples, n_features)
                TODO

        Returns
        -------
            topics : torch.tensor, shape=(n_samples,)
                TODO
        """

        topics = self.slda.transform(X)

        return topics
