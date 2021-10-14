import numpy as np
from matplotlib import pyplot as plt

# A Q-Q plot is a scatterplot created by plotting two sets of quantiles against one another. If both sets of quantiles came from the same distribution, we should see the points forming a line that’s roughly straight. 
    

def qqplot(
    x,
    y,
    quantiles=None,
    interpolation="nearest",
    ax=None,
    rug=False,
    rug_length=0.05,
    rug_kwargs=None,
    **kwargs
):
    

    # Get current axes if none are provided
    if ax is None:
        ax = plt.gca()

    if quantiles is None:
        # quantiles = min(len(x), len(y))
        quantiles = 10

    # Compute quantiles of the two samples

    quantiles_num = np.linspace(start=0, stop=1, num=int(quantiles))

    x_quantiles = np.quantile(x, quantiles_num, interpolation=interpolation)
    y_quantiles = np.quantile(y, quantiles_num, interpolation=interpolation)

    # Draw the rug plots if requested
    if rug:
        # Default rug plot settings
        rug_x_params = dict(ymin=0, ymax=rug_length, c="gray", alpha=0.5)
        rug_y_params = dict(xmin=0, xmax=rug_length, c="gray", alpha=0.5)

        # Override default setting by any user-specified settings
        if rug_kwargs is not None:
            rug_x_params.update(rug_kwargs)
            rug_y_params.update(rug_kwargs)

        # Draw the rug plots
        for point in x:
            ax.axvline(point, **rug_x_params)
        for point in y:
            ax.axhline(point, **rug_y_params)

    # Draw the q-q plot

    ax.loglog(x_quantiles, y_quantiles, basex=10, basey=10, **kwargs)
