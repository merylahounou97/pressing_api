# Processus de création de test

## Entité( User, Order)

Pour créer le test dans une entité, on crée une classe dans laquelle on gère toutes les dépendances commune aux tests.
Ensuite on crée une classe Test dans laquelle on écrit tous les tests, et dans ce cas le seul paramètre est le fixture factory de la classe associée

## Exemple

Pour créer les tests liés à [users](../src/users),
on a créer une classe [serviceTest](users/test_user_router.py)
pour cette classe on crée un fixture [factory du service](users/fixtures/others/user_test_service_factory.py)
Et ce factory est en paramètre pour chaque test écrit dans [la classe de test](users/test_user_router.py)