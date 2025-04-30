## Statistics on Growth Data

Visualized data collected from 2023/07/07 - 2025/04/29, 1458 records from 29 kittens from 9 litters.

### Mixed-effect Model of Growth
{::nomarkdown}
Null Hypothesis $H_0$: $weight \sim (1 \mid id)$

Alternative Hypothesis $H_1$: $weight \sim ageInDays + birthWeight + hairType + hairColor + monthOfBirth + (1 \mid id)$
{:/}
{% include_relative _graphs/2025-04-29_model-fitness.html %}

### Visualization

{% include_relative _graphs/2025-04-29_growth-curve.html %}

{% include_relative _graphs/2025-04-29_born-weights-distribution.html %}
