import arcpy
import os

aprx = arcpy.mp.ArcGISProject("CURRENT")
nr_planu= arcpy.GetParameterAsText(0)
mpzpMap = aprx.listMaps("{}_MPZP".format(nr_planu))[0]

folder = aprx.homeFolder
arcpy.env.workspace = r"{}\brg_mpzp.gdb".format(folder)
arcpy.env.overwriteOutput = True
workspace = arcpy.env.workspace
skala = arcpy.GetParameterAsText(1)

ptPodzwew = mpzpMap.listLayers("PUNKTY_PODZ_WEW")[0]
opDod = mpzpMap.listLayers("OPISY_DOD")[0]
ptSrodInf = mpzpMap.listLayers("PUNKTY_SROD_INFO")[0]
mz = mpzpMap.listLayers("MAPA_ZASADNICZA")[0]
przez = mpzpMap.listLayers("PRZEZ")[0]
przezUl = mpzpMap.listLayers("PRZEZ_ULICE")[0]
przezInfr = mpzpMap.listLayers("PRZEZ_INFR")[0]
przezKom = mpzpMap.listLayers("PRZEZ_KOM")[0]
rob = mpzpMap.listLayers("ROBOCZE")[0]
gran = mpzpMap.listLayers("GRANICA")[0]
punkty = mpzpMap.listLayers("PUNKTY")[0]

if f"PODKLAD_{nr_planu}.tif" in [layer.name for layer in mpzpMap.listLayers()]:
    rast = mpzpMap.listLayers(f"PODKLAD_{nr_planu}.tif")[0]
    rast.name = f"PODKLAD_{nr_planu}"
elif f"PODKLAD_{nr_planu}" in [layer.name for layer in mpzpMap.listLayers()]:
    rast = mpzpMap.listLayers(f"PODKLAD_{nr_planu}")[0]
else:
    pass
if "BAZA_ADRESOWA" in [layer.name for layer in mpzpMap.listLayers()]:
    bazAd = mpzpMap.listLayers("BAZA_ADRESOWA")[0]
else:
    pass
if "EWIDENCJA_GRUNTOW" in [layer.name for layer in mpzpMap.listLayers()]:
    ewGrunt = mpzpMap.listLayers("EWIDENCJA_GRUNTOW")[0]
else:
    pass
if "BUDYNKI_EWIDENCYJNE" in [layer.name for layer in mpzpMap.listLayers()]:
    budEw = mpzpMap.listLayers("BUDYNKI_EWIDENCYJNE")[0]
else:
    pass
if "PRZEZ_MIX" in [layer.name for layer in mpzpMap.listLayers()]:
    przezMix = mpzpMap.listLayers("PRZEZ_MIX")[0]
else:
    pass

camera = aprx.activeView.camera
camera.setExtent(arcpy.Describe(rast).extent)

ptPodzwew.visible = False
opDod.visible = False
ptSrodInf.visible = False
mz.visible = False
rob.visible = False
punkty.visible = False

if "BAZA_ADRESOWA" in [layer.name for layer in mpzpMap.listLayers()]:
    bazAd.visible = False
else:
    pass
if "EWIDENCJA_GRUNTOW" in [layer.name for layer in mpzpMap.listLayers()]:
    ewGrunt.visible = False
else:
    pass
if "BUDYNKI_EWIDENCYJNE" in [layer.name for layer in mpzpMap.listLayers()]:
    budEw.visible = False
else:
    pass

przez.showLabels = True
przezUl.showLabels = True
przezInfr.showLabels = True
przezKom.showLabels = True

if "PRZEZ_MIX" in [layer.name for layer in mpzpMap.listLayers()]:
    przezMix.showLabels = True
else:
    pass

mpzpMap.clearSelection()

if arcpy.Exists(r"{}\opisy_przeznaczenia".format(workspace)):
    pass 
else:
    arcpy.cartography.ConvertLabelsToAnnotation("{}_MPZP".format(nr_planu), skala, workspace, "Opis", "6527901.82 6016246.08 6561773.11 6035325.6", "ONLY_PLACED", "NO_REQUIRE_ID", "STANDARD", "AUTO_CREATE", "SHAPE_UPDATE", "OPISY", "ALL_LAYERS", None, "SINGLE_FEATURE_CLASS", "MERGE_LABEL_CLASS")
    arcpy.management.Rename(r"{}\T{}_MPZPOpis".format(workspace, nr_planu), r"{}\OPISY".format(workspace), "FeatureClass")
    op_przez = r"{}\OPISY".format(workspace)
    mpzpMap.addDataFromPath(op_przez)
    OpisyPrzez = mpzpMap.listLayers("OPISY")[0]
    cl = mpzpMap.listLayers("Class 1")[0]
    cl.name = "opisy_przeznaczenia"

przez.showLabels = False
przezUl.showLabels = False
przezInfr.showLabels = False
przezKom.showLabels = False
if "PRZEZ_MIX" in [layer.name for layer in mpzpMap.listLayers()]:
    przezMix.showLabels = False
else:
    pass

ptPodzwew.visible = True
opDod.visible = True
ptSrodInf.visible = True
punkty.visible = True

ptPodzwew.showLabels = True
opDod.showLabels = True
ptSrodInf.showLabels = True

arcpy.AddMessage(nr_planu)
arcpy.AddMessage(skala)
arcpy.AddMessage("Brawo! Elegancko zamienione etykiety na opisy")
