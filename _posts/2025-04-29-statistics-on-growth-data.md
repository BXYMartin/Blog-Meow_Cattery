## Statistics on Growth Data

Visualized data collected from 2023/07/07 - 2025/04/29, 1458 records from 29 kittens from 9 litters.

### Mixed-effect Model of Growth

Null Hypothesis

\begin{equation*}
weight \sim (1 \mid id)
\end{equation*}

Alternative Hypothesis

\begin{equation*}
weight \sim age\_in\_days + birth\_weight + hair\_type + hair\_color + month\_of\_birth + (1 \mid id)
\end{equation*}

### Visualization

{% include_relative _graphs/2025-04-29_growth-curve.html %}

{% include_relative _graphs/2025-04-29_born-weights-distribution.html %}
