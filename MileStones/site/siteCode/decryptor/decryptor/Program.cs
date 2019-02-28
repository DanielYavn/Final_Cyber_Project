using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Reflection;
using System.IO;
using System.Net.Http;



namespace decryptor
{
    class Program
    {
        static void Main(string[] args)
        {
            string url = "http://127.0.0.1:5000/run_permission/";
            int id = 1;
            //Console.WriteLine("starting communictaion");
            string key = Communication.GetKey(url + id.ToString());
            //Console.WriteLine("end key is: "+key);

            if (key == "")
            {
                Console.WriteLine("In order to play the game you have to buy it");
            }
            else
            {
                byte[] code = RunGame.GetUnencryptGame("");
                RunGame.RunCSExe(code);
            }
            Console.ReadLine();


        }
    }
    class Communication
    {

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

    }
    class RunGame
    {
        static string path = @".\game.deg";
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
        public static byte[] GetUnencryptGame(string key)
        {
            FileStream fs = new FileStream(path, FileMode.Open);
            BinaryReader br = new BinaryReader(fs);

            byte[] contents = br.ReadBytes(Convert.ToInt32(fs.Length));            
            fs.Close();
            br.Close();
            return contents;
        }

       
    }
}