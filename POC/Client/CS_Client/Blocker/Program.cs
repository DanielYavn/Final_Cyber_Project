using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Diagnostics;
using System.Reflection;
using System.IO;

namespace Client
{
    class Program
    {

        static void Main(string[] args)
        {
           
            try
            {
                //reguest prommition
                string key = Communication.GetEKey();
                //unincript
                byte[] code = returnUnincripted(key);
                RunGame.RunCSExe(code);
            }
            catch (KeyDeniedException)
            {
                Console.WriteLine("In order to play the game you have to by it");
            }
            


        }
        static byte[] returnUnincripted(string key)
        {
            FileStream fs = new FileStream(@"..\EncriptedSimpleGame.txt", FileMode.Open);
            BinaryReader br = new BinaryReader(fs);
            byte[] contents = br.ReadBytes(Convert.ToInt32(fs.Length));            //unincript
            fs.Close();
            br.Close();
            return contents;
        }
    }
}
