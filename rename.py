import os
import exifread
import sys

# Add Standard folder here for fallback
standard_folder = ""

# check if argument has been passed 
if(len(sys.argv))>1:
    folder = sys.argv[1]
    if not os.path.isdir(folder):
        print("Passed argument \"{0}\" is not a valid folder!".format(sys.argv[1]))
        folder = standard_folder
    else:
        print("Passed folder is {0}".format(sys.argv[1]))


if os.path.isdir(folder):
    count = 0
    for i in os.listdir(folder):
        
        
        f = folder + "\\" + i

        if not os.path.isfile(f): # Skip if it is a folder
            continue

        try:    
            # Open image file for reading (binary mode)
            p = open(f, 'rb')

            # Return Exif tags
            tags = exifread.process_file(p)
            
            meta = tags["EXIF DateTimeOriginal"]
            metasub = tags["EXIF SubSecTimeOriginal"]

            # make string
            meta = str(meta)
            metasub = str(metasub)

            # Remove 3rd subsecond to match already existing files    
            metasub = metasub[:-1] 

            # Concatenate
            metastring = meta + metasub
            
            # Replace : and blank in new string
            newname = metastring.replace(":","")
            newname = newname.replace(" ", "_")

            # Build complete name
            newname = folder + "\\" + newname + ".jpg"
            
            # Close file before renaming it
            p.close()

            # Rename it and count, but only if renamed
            if (f != newname):
                os.rename(f,newname)
                count = count + 1
        
        except:
            print("Skipping ", f, end=' ')
            print(sys.exc_info()[0])
            continue

    print("Files renamed: ", end='')
    print(count)
else:
    print("Folder \"{0}\" does not exist!!".format(folder))
