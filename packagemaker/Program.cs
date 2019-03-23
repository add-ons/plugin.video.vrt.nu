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
        private const string ZipfileName = "plugin.video.vrt.nu.zip";
        private const string SubFolderName = "plugin.video.vrt.nu";
        private const string ZipFolderName = "zip";

        static void Main(string[] args)
        {
            var dllLocation = Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location);

            var rootFolder = Path.Combine(dllLocation, @"..");
#if DEBUG
            rootFolder = Path.Combine(dllLocation, @"..", @"..", @"..", @"..");
#endif
            rootFolder = Path.GetFullPath(rootFolder);//gives nicer output in logs

            var destination = Path.Combine(rootFolder, ZipFolderName, SubFolderName);

            var zipDestination = Path.Combine(rootFolder, ZipFolderName, ZipfileName);
            RemoveDestinationZip(zipDestination);

            var vrtPluginRoot = Path.Combine(rootFolder, SubFolderName);

            var copiedFiles = CopyFilesToDestination(rootFolder, vrtPluginRoot, destination);
            DeleteUnecesaryFiles(destination, copiedFiles);

            CreateZipFile(zipDestination, destination);
            
            RemoveDestinationDirectory(destination);

            Console.WriteLine($"Created zip at {Path.GetFullPath(zipDestination)}");
            Console.WriteLine("Type any key to exit");
            Console.ReadLine();
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

            Console.WriteLine("Deletings tests folder");
            Directory.Delete(Path.Combine(destination, "vrtnutests"), true);
        }

        private static string[] CopyFilesToDestination(string root, string pluginVideoVrtNuRoot, string destination)
        {
            DirectoryCopy(pluginVideoVrtNuRoot, destination, true);

            File.Copy(Path.Combine(root, "LICENSE"), Path.Combine(destination, "LICENSE"));
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
