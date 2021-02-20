# Clutering de positions basé sur une indexation QuadTree

Ceci est une expérimentation de déduction de clustering par l'usage de la [structure de données quadtree](https://fr.wikipedia.org/wiki/Quadtree)

Pour tester l'expérimentation:

```
▶ python3 app.py result.csv --layer 20
```

avec `result.csv` devant contenir une serie de position sous la forme.

```
timestamp,lat,lng,accuracy
1610790065212,47.6912261,-2.3685829,34.4
...
```