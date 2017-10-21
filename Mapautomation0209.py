path = r"C:Student\MapScripting10_0\Maps\\"
arcpy.env.workspace = path
sourceLyr = arcpy.mapping.Layer(r"C:Student\MapScripting10_0\NewParks.lyr")
for mapDoc in arcpy.ListFiles("*.mxd"):
    print mapDoc
    mxd = arcpy.mapping.MapDocument(path + mapDoc)
    for df in arcpy.mapping.ListDataframes(mxd):
        updateLyr = arcpy.mapping.ListLayers(mxd, "Parks", df)[0]
        arcpy.mapping.UpdateLayer(df, updateLyr, sourceLyr)
    mxd.save()
    del mxd
del sourceLyr
