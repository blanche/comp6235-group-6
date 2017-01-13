/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package foundationjusteatscrap;
import GNM.GNM;
import com.sun.rowset.internal.Row;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.List;
import javafx.scene.control.Cell;  

/**
 *
 * @author Ut
 */
public class TxtWriter {

    public static void main(String[] args) throws InterruptedException, FileNotFoundException, IOException {

        //PrintWriter writer = new PrintWriter("the-file-name.txt", "UTF-8");
        /*PrintWriter writer = new PrintWriter(new FileOutputStream(
                new File("the-file-namzze.txt"),
                true ));
        writer.println("The first line");
        writer.println("The second lineaa");
        writer.close();
         */
        /*
        BufferedReader in = new BufferedReader(new FileReader("the-file-namzze.txt"));
        String line;
        while ((line = in.readLine()) != null) {
            System.out.println(line);
        }
        in.close();
        */
        /*
        Boolean x = GNM.FileExists("C:\\Users\\Ut\\Documents\\NetBeansProjects\\FoundationJustEatScrap", "Aberdeen_Tes1.xls");
        System.out.println(x);
        */
        //File varTmpDir = new File("C:\\Users\\Ut\\Documents\\NetBeansProjects\\FoundationJustEatScrap\\the-file-n2ame.txt");
        //boolean exists = varTmpDir.exists();
        //System.out.println(exists);
        
        String path = "C:\\Users\\Ut\\Documents\\NetBeansProjects\\FoundationJustEatScrap";
        String fileName = "testFile.txt";
        
        PrintWriter writer = new PrintWriter(new FileOutputStream( new File(path + "\\" + fileName), true));
        writer.print("firstsentence");
        writer.print("  ");
        writer.print("sssss");
        writer.close();
        
    }

}
