==================
Class: ``SRAGMap``
==================


.. contents:: Local Navigation
   :local:

Children
========

.. toctree::
   :maxdepth: 1
   
   
Description
===========




.. _SRAGMap.makeMap:


Function: ``makeMap``
=====================

Builds a Brazilian map

.. js:function:: makeMap(geoJsonBr, sragData)

    
    :param dict geoJsonBr: geoJson data about Brazilian territory
    :param dict sragData: SRAG data
    
.. _SRAGMap.getAlertLevelForWholeYear:


Function: ``getAlertLevelForWholeYear``
=======================================

Gets the alert level color using the follow criteria:

- Red (level 4) if the incidence was above the high threshold for at
  least 5 weeks;
- Orange (level 3) if above the high threshold from 1 to 4 weeks;
- Yellow (level 2) if crossed the epidemic threshold but not the high one;
- Green (level 1) if it did not cross the epidemic threshold.

.. js:function:: getAlertLevelForWholeYear(d)

    
    :param dict d: Total number of alert occurrence
    :return number: - Alert level (1-4)
    
.. _SRAGMap.changeColorMap:


Function: ``changeColorMap``
============================

Changes the color of the map using the alerts criteria

.. js:function:: changeColorMap(df)

    
    :param dict df: Data frame object
    

.. _SRAGMap.fluColors:

Member: ``fluColors``: 

.. _SRAGMap.map:

Member: ``map``: 

.. _SRAGMap.osm:

Member: ``osm``: 

.. _SRAGMap.geojsonLayer:

Member: ``geojsonLayer``: 

.. _SRAGMap.regionIds:

Member: ``regionIds``: 

.. _SRAGMap.regionNames:

Member: ``regionNames``: 

.. _SRAGMap.legend:

Member: ``legend``: 

.. _SRAGMap.geojsonLayer:

Member: ``geojsonLayer``: 

.. _SRAGMap.geojsonLayer:

Member: ``geojsonLayer``: 




