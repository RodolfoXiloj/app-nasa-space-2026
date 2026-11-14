// Milpa Resiliente · Cambios proyectados por los modelos de NASA (NEX-GDDP-CMIP6)
// Pegar en https://code.earthengine.google.com, Run y luego RUN a la tarea "milpa_cmip6_cambios".
// Para cada parcela, modelo y escenario saca la lluvia media de mayo-octubre y de junio-agosto
// (canícula) y la temperatura media de mayo-octubre, en 1995-2014 (base) y 2041-2060.
// El motor convierte eso en cambio % de lluvia y +°C por modelo (pipeline/cmip6.py).

var PARCELAS = ee.FeatureCollection([
  ee.Feature(ee.Geometry.Point([-89.39433, 14.81146]), {parcela: 'jocotan'}),
  ee.Feature(ee.Geometry.Point([-89.37404, 14.86146]), {parcela: 'camotan'}),
  ee.Feature(ee.Geometry.Point([-89.29358, 14.66563]), {parcela: 'olopa'}),
  ee.Feature(ee.Geometry.Point([-89.42065, 14.78646]), {parcela: 'san_juan_ermita'}),
  ee.Feature(ee.Geometry.Point([-89.56, 14.94062]), {parcela: 'zacapa'})
]);
var CMIP6 = ee.ImageCollection('NASA/GDDP-CMIP6');
var MODELOS = CMIP6.filterDate('2000-01-01', '2000-01-02').aggregate_array('model').distinct();

function medias(modelo, escenario, inicio, fin) {
  var col = CMIP6.filter(ee.Filter.eq('model', modelo)).filter(ee.Filter.eq('scenario', escenario))
    .filterDate(inicio, fin).select(['pr', 'tas']);
  var mayOct = col.filter(ee.Filter.calendarRange(5, 10, 'month')).mean();
  var junAgo = col.filter(ee.Filter.calendarRange(6, 8, 'month')).select('pr').mean();
  var img = mayOct.select('pr').multiply(86400).rename('pr_may_oct_mm_dia')
    .addBands(junAgo.multiply(86400).rename('pr_jun_ago_mm_dia'))
    .addBands(mayOct.select('tas').subtract(273.15).rename('tas_may_oct_c'));
  var fc = img.reduceRegions({collection: PARCELAS, reducer: ee.Reducer.first(), scale: 27830})
    .map(function (f) { return f.set({modelo: modelo, escenario: escenario}).setGeometry(null); });
  // HadGEM3-GC31-MM no tiene ssp245: se salta en vez de fallar.
  return ee.FeatureCollection(ee.Algorithms.If(col.size().gt(0), fc, ee.FeatureCollection([])));
}

var tabla = ee.FeatureCollection(MODELOS.map(function (m) {
  return ee.FeatureCollection([
    medias(m, 'historical', '1995-01-01', '2015-01-01'),
    medias(m, 'ssp245', '2041-01-01', '2061-01-01'),
    medias(m, 'ssp585', '2041-01-01', '2061-01-01')
  ]).flatten();
})).flatten();

print('Modelos:', MODELOS.size());

Export.table.toDrive({
  collection: tabla,
  description: 'milpa_cmip6_cambios',
  folder: 'milpa_resiliente',
  fileFormat: 'CSV',
  selectors: ['parcela', 'modelo', 'escenario', 'pr_may_oct_mm_dia', 'pr_jun_ago_mm_dia', 'tas_may_oct_c']
});
