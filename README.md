# GraphQL Project

Welcome to the GraphQL Project! This repository contains code and information about using GraphQL in your application.

## Getting Started

Follow these steps to get started with the GraphQL project:

1. Clone the repository

2. In root directory run docker-compose up --build

## Api requests examples 

1. Get person by ID

{
  "query": "query getPerson($id: String!) { getPerson(id: $id) { id name surname dates { lastlogin register } } }",
  "variables": {
    "id": "user id"
  }
}

2. Get list of all persons 

{
  "query": "query getAllPersons($name: String, $surname: String, $page: Int, $limit: Int) { getAllPersons(name: $name, surname: $surname, page: $page, limit: $limit) { id name surname dates { lastlogin register } } }",
  "variables": {
    "name": "user name",
    "surname": "user surname",
    "page": number of page,
    "limit": number limit of users/page
  }
}

3. Create user

{
  "query": "mutation createPerson($name: String!, $surname: String!) { createPerson(name: $name, surname: $surname) { person { id name surname dates { lastlogin register } } } }",
  "variables": {
    "name": "user name",
    "surname": "user surname"
  }
}

4. Update user

{
  "query": "mutation updatePerson($id: String!, $name: String, $surname: String) { updatePerson(id: $id, name: $name, surname: $surname) { person { id name surname dates { lastlogin register } } } }",
  "variables": {
    "id": "64e6fef59c4d3f5204f14c93",
    "name": "user name",
    "surname": "user surname"
  }
}

5. Delete user

{
  "query": "query getPerson($id: String!) { getPerson(id: $id) { id name surname dates { lastlogin register } } }",
  "variables": {
    "id": "user id"
  }
}