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

ptPodzwew.visible = False
opDod.visible = False
ptSrodInf.visible = False
mz.visible = False

mpzpMap.clearSelection()

if arcpy.Exists(r"{}\opisy_przeznaczenia".format(workspace)):
    pass 
else:
    arcpy.cartography.ConvertLabelsToAnnotation("{}_MPZP".format(nr_planu), skala, workspace, "Opis", "6527901.82 6016246.08 6561773.11 6035325.6", "ONLY_PLACED", "NO_REQUIRE_ID", "STANDARD", "AUTO_CREATE", "SHAPE_UPDATE", "OPISY", "ALL_LAYERS", None, "SINGLE_FEATURE_CLASS", "MERGE_LABEL_CLASS")

    arcpy.management.Rename(r"{}\T{}_MPZPOpis".format(workspace, nr_planu), r"{}\opisy_przeznaczenia".format(workspace), "FeatureClass")

    MPZPopisLyr = mpzpMap.listLayers("T{}_MPZPOpis".format(nr_planu))[0]

    mpzpMap.removeLayer(MPZPopisLyr)

    op_przez = r"{}\opisy_przeznaczenia".format(workspace)
    
    OpisyLyr = mpzpMap.listLayers("OPISY")[0]
    
    mpzpMap.addDataFromPath(op_przez)
    
    OpisyPrzez = mpzpMap.listLayers("opisy_przeznaczenia")[0]

    mpzpMap.addLayerToGroup(OpisyLyr, OpisyPrzez)
    mpzpMap.removeLayer(OpisyPrzez)

przez = True
przezUl = True
przezInfr = True
przezKom = True

ptPodzwew.showLabels = True
opDod.showLabels = True
ptSrodInf.showLabels = True

arcpy.AddMessage(nr_planu)
arcpy.AddMessage(skala)
arcpy.AddMessage("Brawo! Elegancko zamienione etykiety na opisy")
