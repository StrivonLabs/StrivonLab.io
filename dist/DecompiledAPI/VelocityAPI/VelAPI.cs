using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Net.Http;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading.Tasks;
using System.Timers;
using coms;

namespace VelocityAPI;

public class VelAPI
{
	private HttpClient client = new HttpClient();

	private string current_version_url = "https://realvelocity.xyz/assets/current_version.txt";

	private string current_download_links_url = "https://realvelocity.xyz/assets/download_links.json";

	private Process decompilerProcess;

	public VelocityStates VelocityStatus = VelocityStates.NotAttached;

	public List<int> injected_pids = new List<int>();

	private Timer CommunicationTimer;

	public static string Base64Encode(string plainText)
	{
		return Convert.ToBase64String(Encoding.UTF8.GetBytes(plainText));
	}

	private static DownloadUrlData ParseJson(string json)
	{
		return new DownloadUrlData
		{
			L1 = Get("L1"),
			L2 = Get("L2"),
			question = Get("question")
		};
		string Get(string key)
		{
			Match match = Regex.Match(json, "\"" + key + "\"\\s*:\\s*\"(.*?)\"");
			if (!match.Success)
			{
				return null;
			}
			return match.Groups[1].Value;
		}
	}

	public static byte[] Base64Decode(string plainText)
	{
		return Convert.FromBase64String(plainText);
	}

	private bool IsPidRunning(int pid)
	{
		try
		{
			Process.GetProcessById(pid);
			return true;
		}
		catch (ArgumentException)
		{
			return false;
		}
	}

	private void AutoUpdate()
	{
		string text = "";
		HttpResponseMessage result = client.GetAsync(current_download_links_url).Result;
		DownloadUrlData downloadUrlData = ParseJson(result.Content.ReadAsStringAsync().Result);
		string requestUri = AESEncryption.Decrypt(downloadUrlData.L1, downloadUrlData.question);
		string requestUri2 = AESEncryption.Decrypt(downloadUrlData.L2, downloadUrlData.question);
		try
		{
			text = client.GetStringAsync(current_version_url).Result;
		}
		catch (Exception)
		{
			return;
		}
		string text2 = "";
		if (File.Exists("Bin\\current_version.txt"))
		{
			text2 = File.ReadAllText("Bin\\current_version.txt");
		}
		if (text != text2)
		{
			if (File.Exists("Bin\\erto3e4rortoergn.exe"))
			{
				File.Delete("Bin\\erto3e4rortoergn.exe");
			}
			if (File.Exists("Bin\\Decompiler.exe"))
			{
				File.Delete("Bin\\Decompiler.exe");
			}
			HttpResponseMessage result2 = client.GetAsync(requestUri2).Result;
			if (result.IsSuccessStatusCode)
			{
				byte[] result3 = result2.Content.ReadAsByteArrayAsync().Result;
				File.WriteAllBytes("Bin\\erto3e4rortoergn.exe", result3);
			}
			HttpResponseMessage result4 = client.GetAsync(requestUri).Result;
			if (result.IsSuccessStatusCode)
			{
				byte[] result5 = result4.Content.ReadAsByteArrayAsync().Result;
				File.WriteAllBytes("Bin\\Decompiler.exe", result5);
			}
		}
		File.WriteAllText("Bin\\current_version.txt", text);
	}

	public void StartCommunication()
	{
		if (!Directory.Exists("Bin"))
		{
			Directory.CreateDirectory("Bin");
		}
		if (!Directory.Exists("AutoExec"))
		{
			Directory.CreateDirectory("AutoExec");
		}
		if (!Directory.Exists("Workspace"))
		{
			Directory.CreateDirectory("Workspace");
		}
		if (!Directory.Exists("Scripts"))
		{
			Directory.CreateDirectory("Scripts");
		}
		AutoUpdate();
		StopCommunication();
		decompilerProcess = new Process();
		decompilerProcess.StartInfo.FileName = "Bin\\Decompiler.exe";
		decompilerProcess.StartInfo.UseShellExecute = false;
		decompilerProcess.EnableRaisingEvents = true;
		decompilerProcess.StartInfo.RedirectStandardError = true;
		decompilerProcess.StartInfo.RedirectStandardInput = true;
		decompilerProcess.StartInfo.RedirectStandardOutput = true;
		decompilerProcess.StartInfo.CreateNoWindow = true;
		decompilerProcess.Start();
		CommunicationTimer = new Timer(100.0);
		CommunicationTimer.Elapsed += delegate
		{
			foreach (int injected_pid in injected_pids)
			{
				if (!IsPidRunning(injected_pid))
				{
					injected_pids.Remove(injected_pid);
				}
			}
			string plainText = "setworkspacefolder: " + Directory.GetCurrentDirectory() + "\\Workspace";
			foreach (int injected_pid2 in injected_pids)
			{
				NamedPipes.LuaPipe(Base64Encode(plainText), injected_pid2);
			}
		};
		CommunicationTimer.Start();
	}

	public void StopCommunication()
	{
		if (CommunicationTimer != null)
		{
			CommunicationTimer.Stop();
			CommunicationTimer = null;
		}
		if (decompilerProcess != null)
		{
			decompilerProcess.Kill();
			decompilerProcess.Dispose();
			decompilerProcess = null;
		}
		injected_pids.Clear();
	}

	public bool IsAttached(int pid)
	{
		return injected_pids.Contains(pid);
	}

	public async Task<VelocityStates> Attach(int pid)
	{
		if (injected_pids.Contains(pid))
		{
			return VelocityStates.Attached;
		}
		VelocityStatus = VelocityStates.Attaching;
		Process.Start(new ProcessStartInfo
		{
			FileName = "Bin\\erto3e4rortoergn.exe",
			Arguments = $"{pid}",
			CreateNoWindow = false,
			UseShellExecute = false,
			RedirectStandardError = false,
			RedirectStandardOutput = false
		}).WaitForExit();
		injected_pids.Add(pid);
		VelocityStatus = VelocityStates.Attached;
		return VelocityStates.Attached;
	}

	public VelocityStates Execute(string script)
	{
		if (injected_pids.Count.Equals(0))
		{
			return VelocityStates.NotAttached;
		}
		foreach (int injected_pid in injected_pids)
		{
			NamedPipes.LuaPipe(Base64Encode(script), injected_pid);
		}
		return VelocityStates.Executed;
	}
}
