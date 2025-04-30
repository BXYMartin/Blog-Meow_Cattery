## Statistics on Growth Data

Visualized data collected from 2023/07/07 - 2025/04/29, 1458 records of 29 kittens from 9 litters.

### Mixed-effect Model of Growth

Null Hypothesis \\(H_0\\)
{::nomarkdown}
\begin{equation*}
weight \sim (1 \mid id)
\end{equation*}
{:/}

Alternative Hypothesis \\(H_1\\)

{::nomarkdown}
\begin{equation*}
weight \sim ageInDays + birthWeight + hairType + hairColor + monthOfBirth + (1 \mid id)
\end{equation*}
{:/}

{% include_relative _graphs/2025-04-29_model-fitness.html %}

We have observed a very strong correlation between the age (days) and the recorded weights, with an average growth of **11.71 g/day**.

We have also seen a strong correlation between the weight of birth to the rate of growth for the kittens in the first 60 days. From the confidence interval of `birth_weight`, we can see that kittens born with a heavier body weight tend to grow faster than the other kittens.

### Visualization

{% include_relative _graphs/2025-04-29_growth-curve.html %}

{% include_relative _graphs/2025-04-29_born-weights-distribution.html %}

We have seen a trend that male kittens tend to have heavier body weight when they were born.
