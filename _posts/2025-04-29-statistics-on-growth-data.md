## Statistics on Growth Data

Visualized data collected from 2023/07/07 - 2025/04/29, 1458 records from 29 kittens from 9 litters.

### Mixed-effect Model of Growth

Null Hypothesis

$weight ~ (1 | id)$

Alternative Hypothesis

$weight ~ age_in_days + birth_weight + hair_type + hair_color + month_of_birth + (1 | id)$

### Visualization

{% include_relative _graphs/2025-04-29_growth-curve.html %}

{% include_relative _graphs/2025-04-29_born-weights-distribution.html %}
