"""Motor de Milpa Resiliente: Python puro (biblioteca estándar + PyYAML), sin red.

Recibe datos ya cacheados en data/cache/ y devuelve el JSON del contrato
(contracts/recomendacion.schema.json). La API y la exportación estática llaman a la
misma función: motor.recomendar.recomendar().
"""
VERSION = "0.1.0"
VERSION_CONTRATO = "1.0"
