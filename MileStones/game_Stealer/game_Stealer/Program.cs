using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;
using System.Reflection;


namespace game_Stealer
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("start all");
            string decryptor_path = @"D:\Users\Daniel\Downloads\game.exe";
            decryptor_path = @".\game_Enc.exe";

            byte[] code = GetGame(decryptor_path);

            Console.WriteLine("run");
            RunCSExe(code);

            Console.ReadLine();
        }


        public static void RunCSExe(byte[] code)
        {

            Assembly a = Assembly.Load(code);
            MethodInfo method = a.EntryPoint;

            if (method != null)
            {
                object o = a.CreateInstance(method.Name);

                method.Invoke(o, new object[] { new string[0] });
            }
        }

        static string StealFromRescources(string path, string resName)
        {
            string data = "";
            var assembly = Assembly.LoadFrom(path);
            using (Stream stream = assembly.GetManifestResourceStream(resName))
            {
                using (StreamReader reader = new StreamReader(stream))
                {
                    data = reader.ReadToEnd();
                }

            }
            Console.WriteLine(data);
            return data;
        }

        public static byte[] GetGame(string path)
        {
            Console.WriteLine("read recurces");
            string enc_cipher = StealFromRescources(path, "code");


            // defaults to CBC and PKCS7
            var textEncoder = new UTF8Encoding();

            byte[] bytes = Convert.FromBase64String(enc_cipher);
            return bytes;
        }

    }
}
