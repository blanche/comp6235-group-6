/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package GNM;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.URL;
import java.util.ArrayList;  

public class GNM {

    static public String GetWebsite(String website) {
        URL url;
        InputStream is = null;
        BufferedReader br;
        String line;
        String totalWebsite = null;
        try {
            url = new URL(website);
            is = url.openStream();  // throws an IOException
            br = new BufferedReader(new InputStreamReader(is));

            while ((line = br.readLine()) != null) {
                //System.out.println(line);
                totalWebsite = totalWebsite + "\n " + line;
            }
        } catch (Exception ex) {
            System.err.println("Error with page load.");
        } finally {
            try {
                if (is != null) {
                    is.close();
                }
            } catch (Exception ex) {
                // nothing to see here
            }
        }

        return totalWebsite;
    }
 
    public static void AppendToCsv(String path, String fileName, ArrayList<ArrayList<String>> listToExport) throws FileNotFoundException, IOException {
        PrintWriter writer = new PrintWriter(new FileOutputStream(new File(path + "\\" + fileName), true));

        for (int i = 0; i < listToExport.size(); i++) {//x many Comments
            for (int p = 0; p < listToExport.get(i).size(); p++) {
                    writer.print(listToExport.get(i).get(p));
                    writer.print("|");
            }
            writer.println("");
        }
        writer.close();
    }

    public static boolean FileExists(String path, String fileName) {
        File varTmpDir = new File(path + "\\" + fileName);
        boolean exists = varTmpDir.exists();
        return exists;
    }

    public static void AppendToFile(String path, String fileName, String lineToAdd) throws FileNotFoundException {
        PrintWriter writer = new PrintWriter(new FileOutputStream(
                new File(path + "\\" + fileName),
                true));
        writer.println(lineToAdd);
        writer.close();
    }

    public static void CreateFileWithLine(String path, String fileName, String lineToAdd) throws FileNotFoundException {
        PrintWriter writer = new PrintWriter(new FileOutputStream(
                new File(path + "\\" + fileName),
                true));
        writer.println(lineToAdd);
        writer.close();
    }

    public static ArrayList<String> ReadLinesIntoArrayList(String path, String fileName) throws FileNotFoundException, IOException {
        ArrayList<String> linesList = new ArrayList<String>();
        BufferedReader in = new BufferedReader(new FileReader(path + "\\" + fileName));
        String line;
        while ((line = in.readLine()) != null) {
            linesList.add(line);
        }
        in.close();
        return linesList;
    }
}
