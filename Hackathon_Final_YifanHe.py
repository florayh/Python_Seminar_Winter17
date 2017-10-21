# goal: calculate the Mean density of 9 specific food outlet types
# within 1/2, 1, 3, and 5 miles for each census block group.

# set up environment
import arcpy, os 
from arcpy import env
from arcpy.sa import *
arcpy.env.workspace = r"M:\Private\NRE639_Python\Hackathon.gdb"
arcpy.env.overwriteOutput = True
arcpy.CheckOutExtension("Spatial")

#empty table for append
arcpy.CreateTable_management(r"M:\Private\NRE639_Python\Hackathon.gdb", "Kernel_Mean")
inTable = "Kernel_Mean"
arcpy.AddField_management(in_table = inTable, field_name = "NAME", field_type = "LONG", field_length = 7, field_is_nullable="NULLABLE")
arcpy.AddField_management(in_table = inTable, field_name = "ZONE_CODE", field_type = "LONG", field_is_nullable="NULLABLE")
arcpy.AddField_management(in_table = inTable, field_name = "COUNT", field_type = "LONG", field_is_nullable="NULLABLE")
arcpy.AddField_management(in_table = inTable, field_name = "AREA", field_type = "DOUBLE", field_precision = 0, field_scale = 0, field_is_nullable="NULLABLE")
arcpy.AddField_management(in_table = inTable, field_name = "MEAN", field_type = "DOUBLE", field_precision = 0, field_scale = 0, field_is_nullable="NULLABLE")
arcpy.AddField_management(in_table = inTable, field_name = "TYPE", field_type = "TEXT", field_is_nullable="NULLABLE")
arcpy.AddField_management(in_table = inTable, field_name = "DISTANCE", field_type = "LONG", field_is_nullable="NULLABLE")
del(inTable)

# kernel density
types = ['ram', 'bak', 'cat', 'fas', 'far', 'fmk', 'sup', 'gro', 'ebt']
distance = [805, 1609, 4828, 8047]
for dt in distance:
    for tp in types:
        inFeature = "foodpts"
        populationField = tp
        cellSize = 100
        searchRadius = dt
        output_name = str(tp)+str(dt)
        outKernel = KernelDensity(inFeature, populationField, cellSize, searchRadius,"SQUARE_KILOMETERS")
        outKernel.save(output_name)
        # alternatively: outKernel.save(r"M:\Private\NRE639_Python\Hackathon.gdb\Kernel"+str(tp)+str(dt) 
        
        # zonal statistics as table
        inZoneData = "bg2010"
        zoneField = "NAME"
        inValueRaster = outKernel
        outTable = "table" + output_name
        outZonal = ZonalStatisticsAsTable(inZoneData, zoneField, inValueRaster, outTable, "NODATA", "MEAN")

        #add food type and distance fields; append table
        arcpy.AddField_management(in_table = outZonal, field_name = "TYPE", field_type = "TEXT", field_is_nullable="NULLABLE")
        arcpy.CalculateField_management(in_table=outZonal, field="TYPE", expression="\"" + str(tp) + "\"", expression_type="PYTHON", code_block="")
        arcpy.AddField_management(in_table = outZonal, field_name = "DISTANCE", field_type = "TEXT", field_is_nullable="NULLABLE")
        arcpy.CalculateField_management(in_table=outZonal, field="DISTANCE", expression= dt, expression_type="PYTHON", code_block="")
        arcpy.Append_management(outZonal, "Kernel_Mean", "NO_TEST","","")

print "Calculation finished"
