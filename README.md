[![Actions Status](https://github.com/HugoTheDeveloper/python-project-83/workflows/hexlet-check/badge.svg)](https://github.com/HugoTheDeveloper/python-project-83/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/7305d20c348d2fda5a47/maintainability)](https://codeclimate.com/github/HugoTheDeveloper/python-project-83/maintainability)
![Continuous integration](https://github.com/HugoTheDeveloper/python-project-83/actions/workflows/continious-integration.yml/badge.svg)

### Showcase
![](https://github.com/HugoTheDeveloper/python-project-83/blob/main/showcase.gif)
### About project:
This app helps analyze SEO usability of website. It's able to find main headline, title and description.

### What is SEO usability and why it is important:
SEO website usability refers to the ability of a website to be optimized for search engines such as Google, Bing, and Yandex. It involves meeting certain requirements that help search engines understand the content of the website and display it in search results. These requirements include the use of keywords, metadata, page titles, and other factors that help search engines understand what the website offers. SEO website usability is important because it helps to improve the visibility of the website in search engines. If a website does not meet the requirements of search engines, it may not be visible enough to users who are searching for information related to its topic. This can lead to a decrease in traffic to the website and a decrease in potential customers. On the other hand, if a website meets the requirements of search engines, it may be better visible in search results, which can lead to an increase in traffic to the website and an increase in potential customers.

### Requirements:
- Python >=3.10
- Pip
- Poetry
- PostgreSQL

### How to install:
>`python3 -m pip install --user git+https://github.com/HugoTheDeveloper/python-project-83.git`

Execute /database.sql . Then create .env file in root of this project.

Add two variables in this config-file: DATABASE_URL and SECRET_KEY.

SECRET_KEY may be generated or manually entered.

>DATABASE_URL should have this format: {provider}://{user}:{password}@{host}:{port}/{db}
>
>For instance, like this:
> 
>DATABASE_URL=postgresql://janedoe:mypassword@localhost:5432/mydb

### [Check out in action](https://page-analyzer-wf2q.onrender.com)



