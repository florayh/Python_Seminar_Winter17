import arcpy
arcpy.env.workspace = "C:\Data\PythonGP10_0\Data\SanJuan.gdb"
arcpy.env.overwriteOutput = True

# describe 
desc = arcpy.Describe("C:\Data\PythonGP10_0\Data\SanJuan.gdb\Lakes")
print(desc.shapeType)

# create list of feature classes
fcList = arcpy.ListFeatureClasses()
print(fcList)

# print spatial references
for fc in fcList:
    desc = arcpy.Describe(fc)
    print(desc.spatialReference.Name)

# create a loop to buffer lakes and streams
bufferList = []
for fc in fcList:
    if fc == "Lakes" or fc == "Streams":
        arcpy.Buffer_analysis(fc, fc + "Buffer", "1000 meters", dissolve_option = "ALL")
        bufferList.append(fc + "Buffer")
arcpy.Union_analysis(bufferList, "WaterBuffers")


# join bufferdistance table to the roads (need to close ArcMap)
arcpy.JoinField_management("Roads", "ROUTE_TYPE", "BufferDistance", "ROUTE_TYPE")

# Buffer the roads based on DISTANCE attribute
arcpy.Buffer_analysis("Roads","RoadBuffers","DISTANCE")

# Union feature classes
treatmentList = ["RoadBuffers", "WaterBuffers"]
arcpy.Union_analysis(treatmentList, "NonChemical")

