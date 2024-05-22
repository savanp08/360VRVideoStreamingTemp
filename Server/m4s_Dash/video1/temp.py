import os
import subprocess

def concat_m4s_to_mp4():
    """
    Concatenate each .m4s segment with Header.m4s to create individual .mp4 files.

    Parameters:
    directory (str): The path to the directory containing the .m4s segments and Header.m4s.
    """
    header_file = os.path.join( "Header.m4s")

    if not os.path.exists(header_file):
        print(f"{header_file} does not exist")
        return

    # Loop through all files in the given directory
    for root, _, files in os.walk("./"):
        for file in files:
            if file.endswith(".m4s") and file != "Header.m4s":
                segment_file = os.path.join(root, file)
                combined_file = os.path.join(root, "combined.m4s")
                output_file = os.path.join(root, f"{os.path.splitext(file)[0]}.mp4")

                # Concatenate Header.m4s and the segment file into a combined.m4s file using copy command
                cmd = f'copy /b "{header_file}"+"{segment_file}" "{combined_file}"'
                subprocess.run(cmd, shell=True, check=True)

                # Convert the combined.m4s file into an .mp4 file using ffmpeg
                cmd = f'ffmpeg -y -i "{combined_file}" -c copy "{output_file}"'
                subprocess.run(cmd, shell=True, check=True)
                print(f"Created {output_file}")

                # Remove the temporary combined.m4s file
                os.remove(combined_file)

# Set the directory containing the .m4s segments and Header.m4s


# Call the function
concat_m4s_to_mp4()
