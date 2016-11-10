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

Build a map

.. js:function:: makeMap(geoJsonBr, sragData)

    
    :param dict geoJsonBr: geoJson data about Brazilian territory
    :param dict sragData: srag data
    
.. _SRAGMap.getAlertLevelForWholeYear:


Function: ``getAlertLevelForWholeYear``
=======================================

Get the alert level color using the follow criteria:

Red (level 4) if the incidence was above the high threshold for at
 least 5 weeks;
Orange (level 3) if above the high threshold from 1 to 4 weeks;
Yellow (level 2) if crossed the epidemic threshold but not the high one;
Green (level 1) if it did not cross the epidemic threshold.

.. js:function:: getAlertLevelForWholeYear(d)

    
    :param dict d: total number of alert occurrence
    :return number: alert level
    
.. _SRAGMap.changeColorMap:


Function: ``changeColorMap``
============================

Change the color of the map using the alerts criteria

.. js:function:: changeColorMap(df)

    
    :param dict df: data frame object
    

.. _SRAGMap.fluColors:

Member: ``fluColors``: 

.. _SRAGMap.map:

Member: ``map``: 

.. _SRAGMap.osmUrl:

Member: ``osmUrl``: 

.. _SRAGMap.osmAttrib:

Member: ``osmAttrib``: 

.. _SRAGMap.osm:

Member: ``osm``: 

.. _SRAGMap.geojsonLayer:

Member: ``geojsonLayer``: 

.. _SRAGMap.regionIds:

Member: ``regionIds``: 

.. _SRAGMap.regionNames:

Member: ``regionNames``: 

.. _SRAGMap.Legend:

Member: ``Legend``: 

.. _SRAGMap.geojsonLayer:

Member: ``geojsonLayer``: 

.. _SRAGMap.geojsonLayer:

Member: ``geojsonLayer``: 




