/*
 * commpiling with:
 * csc /out:<EndFile.exe> /res:<game.deg>,code /res:<id.txt>,id,private /reference:System.Net.Http.dll /reference:System.Security.Cryptography.Primitives.dll <decryptor.cs>
 * csc /out:EndFile.exe /res:game.deg,code /res:id.txt,id,private /reference:System.Net.Http.dll /reference:System.Security.Cryptography.Primitives.dll decryptor.cs
 * in Developrt command prompt for VS 2017
 */
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
//using System.Threading.Tasks;
using System.Reflection;
using System.IO;
using System.Net.Http;
using System.Security.Cryptography;



namespace decryptor
{
    class Program
    {
        static string url = "http://127.0.0.1:5000/run_permission/";

        static void Main(string[] args)
        {
            Console.WriteLine("start all");
            string id = GetId();
            string[] keyIv = GetKey(url + id).Split( new char [] {'\n'});
            if (keyIv[0] == "")
            {
                Console.WriteLine("In order to play the game you have to buy it");
            }
            else
            {
                byte[] code =  GetGame(keyIv[0], keyIv[1]);
                
                Console.WriteLine("run");
                RunCSExe(code);
            }
            Console.ReadLine();
        }

        public static string GetId()
        {
            var assembly = Assembly.GetExecutingAssembly();
            string id;
            using (Stream stream = assembly.GetManifestResourceStream("id"))
            using (StreamReader reader = new StreamReader(stream))
            {
                id = reader.ReadToEnd();
            }
            return id;
        }
        public static string GetKey(string url)
        {
            string key = "";
            HttpClient client = new HttpClient();
            HttpResponseMessage response;
            try
            {
                response = client.GetAsync(url).Result;
                response.EnsureSuccessStatusCode();
            }
            catch
            {
                Console.WriteLine("communication error");
                return "";
            }
            key = response.Content.ReadAsStringAsync().Result;
            return key;
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
        static string ReadFromRescources(string resName)
        {
            var assembly = Assembly.GetExecutingAssembly();
            string data = "";
            using (Stream stream = assembly.GetManifestResourceStream(resName))
            {
                using (StreamReader reader = new StreamReader(stream))
                {
                    data = reader.ReadToEnd();
                }

            }
            return data;
        }

        public static byte[] GetGame(string key, string iv)
        {
            Console.WriteLine("read rec");
            string enc_cipher = ReadFromRescources("code");
            Console.WriteLine("start decryption");

            Console.WriteLine("key: {0}, iv {1}",key,iv);

            // defaults to CBC and PKCS7
            byte[] encBytes = Convert.FromBase64String(enc_cipher);
           

            return encBytes;
        }

    }
}
