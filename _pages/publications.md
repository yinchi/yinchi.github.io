---
layout: archive
title: "Publications"
permalink: /publications/
author_profile: true
---

**Note**: Papers may appear out of order due to the differences between online and print publication dates.

You can also find my articles on <a href="https://scholar.google.com/citations?user=NJEB3swAAAAJ&hl=en">my Google Scholar profile</a>.

{% include base_path %}

* [Published papers](#published-papers)
* [Preprints](#preprints)

## Published papers

<ol reversed>{% for post in site.publications reversed %}
  <li>{% include archive-single.html %}</li>
{% endfor %}</ol>

## Preprints

<ol reversed>{% for post in site.preprints reversed %}
  <li>{% include archive-single.html %}</li>
{% endfor %}</ol>
