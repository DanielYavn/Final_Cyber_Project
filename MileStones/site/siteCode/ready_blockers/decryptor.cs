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
using System.Reflection;
using System.IO;
using System.Net.Http;
using System.Security.Cryptography;
using System.Windows.Forms;



namespace decryptor
{
    class Program
    {
        static string url = "http://127.0.0.1:5000/run_permission/";

        static void Main(string[] args)
        {
            string id = ReadFromRescurces("id");
            string[] keyIv = null;
            try {
                keyIv = GetKey(url + id).Split(new char[] { '\n' });
            }
            catch (AggregateException)
            {
                server_down_MB();
            }
            if (keyIv[0] == "")
            {
                buy_game_MB();
            }
            else
            {
                byte[] code = GetGame(keyIv[0], keyIv[1]);
                RunCSExe(code);
            }
            }

        public static string GetKey(string url)
        {
            string key = "";
            HttpClient client = new HttpClient();
            HttpResponseMessage response;


            response = client.GetAsync(url).Result;
            response.EnsureSuccessStatusCode();


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
                try
                {
                    method.Invoke(o, null);
                }
                catch
                {
                    method.Invoke(o, new object[] { new string[0] });
                }
                //
            }
        }
        static string ReadFromRescurces(string resName)
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
            string enc_cipher = ReadFromRescurces("code");


            // defaults to CBC and PKCS7
            var textEncoder = new UTF8Encoding();
            var aes = new AesManaged();
            aes.Mode = CipherMode.CBC;
            aes.Padding = PaddingMode.PKCS7;
            aes.Key = textEncoder.GetBytes(key); 
            aes.IV = textEncoder.GetBytes(iv); 

            var decryptor = aes.CreateDecryptor();
            byte[] encBytes = Convert.FromBase64String(enc_cipher);
            byte[] decBytes = decryptor.TransformFinalBlock(encBytes, 0, encBytes.Length);

            byte[] paddingFixer = textEncoder.GetBytes("A_PADDING_FIXER");

            bool paddingFixerExists = true;
            for (int i = 0; i < paddingFixer.Length; i++)
            {
                if (decBytes[decBytes.Length - paddingFixer.Length + i] != paddingFixer[i])
                {
                    paddingFixerExists = false;
                    break;
                }
            }
            byte[] fixedDecBytes;
            if (!paddingFixerExists)
            {
                fixedDecBytes = decBytes;
            }
            else
            {
                fixedDecBytes = new byte[decBytes.Length - paddingFixer.Length];
                for (int i = 0; i < fixedDecBytes.Length; i++)
                {
                    fixedDecBytes[i] = decBytes[i];
                }
            }

            return fixedDecBytes;
        }
        public static void server_down_MB()
        {
            string message = "Could not run the game due to network error. Please check your internet connection and try again later.";
            string caption = "Connection Error";
            MessageBoxButtons buttons = MessageBoxButtons.OK;
            DialogResult result;

            // Displays the MessageBox.
            result = MessageBox.Show(message, caption, buttons);
            System.Environment.Exit(1);
        }
        public static void buy_game_MB()
        {
            string message = "Could not run the game because trial period expired. Please buy the game at our site and try again later.";
            string caption = "Trial Period Expired";
            MessageBoxButtons buttons = MessageBoxButtons.OK;
            DialogResult result;

            // Displays the MessageBox.
            result = MessageBox.Show(message, caption, buttons);
            System.Environment.Exit(1);
        }
    }
}
