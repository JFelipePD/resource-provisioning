package org.cloudbus.cloudsim.forecaster;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;

public class ForecasterRuntime {
    public static String predModel = "";
    public static boolean firstPrediction = true;
    
    public static double Forecast(double[] inputTimeSeries, String predictionModel, int predictionInterval){
        
        predModel = predictionModel;
        // when is the first prediction on the simulation
        if ((firstPrediction == true) && (!predModel.equals("ARIMA"))){
            resetModel();
            firstPrediction = false;
        }
        
        String command = "";
        Double load = 0.0;
    
        double lastValue = 0.0;
        StringBuilder timeSeries = new StringBuilder();
        for (int i = 0; i < inputTimeSeries.length - 1; i++) {
            timeSeries.append(inputTimeSeries[i]).append(',');
            lastValue = inputTimeSeries[i+1];
        }

        String pythonExe = getPythonExecutable();
        String scriptPath = "";

        switch(predictionModel) {
          case "ARIMA":
            scriptPath = resolveFilePath("arima_cloudsim.py");
            command = pythonExe + " " + scriptPath + " " + timeSeries.toString() + lastValue + " " + predictionInterval;
            break;
          case "MLP":
            scriptPath = resolveFilePath("mlp_cloudsim_new.py");
            command = pythonExe + " " + scriptPath + " " + timeSeries.substring(0, Math.max(0, timeSeries.length() - 1)) + " " + lastValue + " " + predictionInterval;    
            break;
          case "GRU":
            scriptPath = resolveFilePath("gru_cloudsim_new.py");
            command = pythonExe + " " + scriptPath + " " + timeSeries.substring(0, Math.max(0, timeSeries.length() - 1)) + " " + lastValue + " " + predictionInterval;
            break;      
          default:
            // code block
        }
        
        System.out.println("Executando: " + command);      
        
        try {
            load = Double.parseDouble(ExecuteCommand(command)); 
        } catch (Exception e) {
            load = lastValue;
        }
            
        return load;
    }
    
    public static String resetModel(){
        if (!predModel.equals("ARIMA")) {
            String fileName = predModel.toLowerCase() + "_cloudsim_new.h5";
            String h5Path = resolveFilePath(fileName);
            File file = new File(h5Path);
            if (file.exists()) {
                file.delete();
                System.out.println("Modelo antigo removido: " + h5Path);
            }
        }
        return "";
    }
    
    public static String ExecuteCommand(String command){
        String result = "";
        try {
            Process process = Runtime.getRuntime().exec(command);
            StringBuilder output = new StringBuilder();
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
    
            String line;
            while ((line = reader.readLine()) != null) {
                output.append(line).append("\n");
            }
    
            int exitVal = process.waitFor();
            String str = output.toString();
            
            if (exitVal == 0) {
                result = str;
            } else {
                System.out.println("Abnormal Execution (Exit code " + exitVal + ")");
            }
    
        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        }
                
        return result.trim();
    }

    /**
     * Identifica o executavel do Python no ambiente (python3 ou python)
     */
    private static String getPythonExecutable() {
        return "python3";
    }

    /**
     * Localiza dinamicamente o arquivo de script ou modelo no projeto
     */
    private static String resolveFilePath(String fileName) {
        String[] locations = {
            "src/org/cloudbus/cloudsim/forecaster/" + fileName,
            "bin/org/cloudbus/cloudsim/forecaster/" + fileName,
            "Kirchoff/src/org/cloudbus/cloudsim/forecaster/" + fileName,
            "Kirchoff/bin/org/cloudbus/cloudsim/forecaster/" + fileName,
            "Kirchoff/" + fileName,
            fileName
        };

        for (String loc : locations) {
            File f = new File(loc);
            if (f.exists()) {
                return f.getAbsolutePath();
            }
        }
        return fileName;
    }
}