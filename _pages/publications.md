---
layout: archive
title: "Publications"
permalink: /publications/
author_profile: true
---

**Note**: Papers may appear out of order due to the differences between online and print publication dates.

You can also find my articles on <a href="https://scholar.google.com/citations?user=NJEB3swAAAAJ&hl=en">my Google Scholar profile</a>.

{% include base_path %}

{% for post in site.publications reversed %}
  {% include archive-single.html %}
{% endfor %}

## Preprints

{% for post in site.preprints reversed %}
  {% include archive-single.html %}
{% endfor %}
