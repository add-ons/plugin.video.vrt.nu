    using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.IO.Compression;
using System.Linq;
using System.Reflection;

namespace plugin.video.vrt.nu.packagemaker
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine(@"Note this program needs to be run from the following path plugin.video.vrt.nu\plugin.video.vrt.nu.packagemaker\bin\Debug\netcoreapp2.1");

            var zipfileName = "plugin.video.vrt.nu.zip";
            var foldername = "plugin.video.vrt.nu";
            var dllLocation = Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location);

            var destination = Path.Combine(dllLocation, foldername);

            RemoveDestinationDirectory(destination);
            RemoveDestinationZip(Path.Combine(dllLocation, zipfileName));

            var copiedFiles = CopyFilesToDestination(dllLocation, foldername, destination);
            DeleteUnecesaryFiles(destination, copiedFiles);

            CreateZipFile(Path.Combine(dllLocation,zipfileName), destination);

            Process.Start("explorer.exe", dllLocation);
        }

        private static void CreateZipFile(string zipfileName, string destination)
        {
            Console.WriteLine("Creating zipfile");
            ZipFile.CreateFromDirectory(destination, zipfileName, CompressionLevel.NoCompression, true);
        }

        private static void DeleteUnecesaryFiles(string destination, IEnumerable<string> copiedFiles)
        {
            foreach (var itemToDelete in copiedFiles.Where(x => x.EndsWith("pyc") || x.EndsWith("pyproj") || x.EndsWith("user")))
            {
                Console.WriteLine($"Deleting {itemToDelete}");
                File.Delete(itemToDelete);
            }

            // Console.WriteLine("Deletings tests folder");
            // Directory.Delete(Path.Combine(destination, "vrtnutests"), true);
        }

        private static string[] CopyFilesToDestination(string dllLocation, string foldername, string destination)
        {
            var root = Path.Combine(dllLocation, @"../../../../");
            var pluginVideoVrtNuRoot = Path.Combine(root, foldername);
            DirectoryCopy(pluginVideoVrtNuRoot, Path.Combine(dllLocation, foldername), true);

            File.Copy(Path.Combine(root, "LICENSE"), Path.Combine(Path.Combine(dllLocation, foldername), "LICENSE"));
            var copiedFiles = Directory.GetFiles(destination, string.Empty, SearchOption.AllDirectories);
            return copiedFiles;
        }

        private static void RemoveDestinationZip(string zipfileName)
        {
            if (File.Exists(zipfileName))
            {
                Console.WriteLine("Removing Zipfile");
                File.Delete(zipfileName);
            }
        }

        private static void RemoveDestinationDirectory(string destination)
        {
            if (Directory.Exists(destination))
            {
                Console.WriteLine("Removing Directory");
                Directory.Delete(destination, true);
            }
        }

        private static void DirectoryCopy(string sourceDirName, string destDirName, bool copySubDirs)
        {
            // Get the subdirectories for the specified directory.
            DirectoryInfo dir = new DirectoryInfo(sourceDirName);

            if (!dir.Exists)
            {
                throw new DirectoryNotFoundException(
                    "Source directory does not exist or could not be found: "
                    + sourceDirName);
            }

            DirectoryInfo[] dirs = dir.GetDirectories();
            // If the destination directory doesn't exist, create it.
            if (!Directory.Exists(destDirName))
            {
                Directory.CreateDirectory(destDirName);
            }

            // Get the files in the directory and copy them to the new location.
            FileInfo[] files = dir.GetFiles();
            foreach (FileInfo file in files)
            {
                string temppath = Path.Combine(destDirName, file.Name);
                file.CopyTo(temppath, false);
            }

            // If copying subdirectories, copy them and their contents to new location.
            if (copySubDirs)
            {
                foreach (DirectoryInfo subdir in dirs)
                {
                    string temppath = Path.Combine(destDirName, subdir.Name);
                    DirectoryCopy(subdir.FullName, temppath, copySubDirs);
                }
            }
        }
    }
}
