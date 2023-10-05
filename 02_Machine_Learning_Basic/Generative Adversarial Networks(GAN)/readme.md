# What is a Generative Model?
+ [developers.google.com](https://developers.google.com/machine-learning/gan/generative)
+ [machinelearningmastery.com](https://machinelearningmastery.com/what-are-generative-adversarial-networks-gans/)
+ ![Generative](Generator_model.png), ![Discriminative](Discriminator_model.png)
+ `Generative` models can generate new data instances.
+ `Discriminative` models discriminate between different kinds of data instances.
+ `Generative` models capture the joint probability p(X, Y), or just p(X) if there are no labels.
+ `Discriminative` models capture the conditional probability p(Y | X).
+ A `generative` model includes the distribution of the data itself, and tells you how likely a given example is
+ A `discriminative` model ignores the question of whether a given instance is likely, and just tells you how likely a label is to apply to the instance

+ Example:
  + generative(unsupervised learning): GAN 
  + discriminative(supervised learning): decision tree
+ Generative Models Are Hard


# Implicit Generative Models vs Explicit(prescribed) Generative Models
+ [EXPLICIT AND IMPLICIT DEEP GENERATIVE MODELS](https://openreview.net/references/pdf?id=RZXkiW1W-)
+ [Implicit Generative Models](https://arxiv.org/pdf/1610.03483.pdf)
+ [Implicit Generative Models](https://casmls.github.io/general/2017/05/24/ligm.html)
+ It is useful to make a distinction between two types of probabilistic models: prescribed and implicit models
  + Implicit generative models use a latent variable z and transform it using a deterministic function Gθ that maps from
  Rm → Rd using parameters θ.
  + Prescribed probabilistic models are those that provide an explicit parametric specification of the
  distribution of an observed random variable x, specifying a log-likelihood function log qθ(x) with parameters θ.

[overview-density-estimation](https://www.kdnuggets.com/2019/10/overview-density-estimation.html)
+ Explicit Density Estimation: MLE, MAP, MOM, KDE, ...
+ Implicit Density Estimation: GAN


# GAN
+ [developers.google.com](https://developers.google.com/machine-learning/gan/generative)
+ [nttuan8.com](https://nttuan8.com/gioi-thieu-series-gan-generative-adversarial-networks/)