pip freeze > .\requirements.txt
#.\update_requirements.ps1
{% comment %} {% extends 'base.html' %}
{% block title %}
Home
{% endblock title %}
{% block body %}
<style>
    table {
        width: 100%;
        border-collapse: collapse;
    }
    th, td {
        padding: 15px;
        text-align: left;
        border-bottom: 1px solid #ddd;
    }
    tr:hover {background-color: #f5f5f5;}
</style>
<table>
    <thead>
        <tr>
            <th>#</th>
            <th>Image</th>
            <th>Name</th>
            <th>Category</th>
            <th>Description</th>
            <th>Process</th>
            <th>Ingredients</th>
        </tr>
    </thead>
    <tbody>
        {% for receipe in receipes %}
        <tr>
            <td>{{ forloop.counter }}</td>
            <td><img src="receipe_image"  width="100"></td>
            <td>{{ receipe.receipe_name }}</td>
            <td>{{ receipe.receipe_category }}</td>
            <td>{{ receipe.receipe_description }}</td>
            <td>{{ receipe.receipe_process }}</td>
            <td>{{ receipe.receipe_ingredients }}</td>
        </tr>
        {% endfor %}
    </tbody>
</table> 
{% endblock body %} {% endcomment %}