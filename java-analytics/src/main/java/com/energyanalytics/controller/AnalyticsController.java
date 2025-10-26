package com.energyanalytics.controller;

import java.io.ByteArrayOutputStream;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Map;

import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.energyanalytics.model.Anomaly;
import com.itextpdf.text.Document;
import com.itextpdf.text.Font;
import com.itextpdf.text.Paragraph;
import com.itextpdf.text.pdf.PdfWriter;

@RestController
@RequestMapping("/api/analytics")
@CrossOrigin(origins = "*")
public class AnalyticsController {

    @GetMapping("/summary")
    public Map<String, Object> getSummary() {
        Map<String, Object> summary = new LinkedHashMap<>();

        double totalConsumption = 123.45;
        double totalGeneration = 98.76;
        double efficiency = (totalGeneration / totalConsumption) * 100;
        String trend = "Decreasing";

        java.util.List<String> recommendations = Arrays.asList(
                "Shift heavy appliance use to off-peak hours.",
                "Increase solar usage during daytime.",
                "Perform maintenance on HVAC systems monthly."
        );

        summary.put("totalConsumption", totalConsumption);
        summary.put("totalGeneration", totalGeneration);
        summary.put("efficiency", efficiency);
        summary.put("trend", trend);
        summary.put("recommendations", recommendations);

        return summary;
    }

    @GetMapping("/anomalies")
    public java.util.List<Anomaly> getAnomalies() {
        java.util.List<Anomaly> anomalies = new ArrayList<>();

        anomalies.add(new Anomaly("17:00", "High Spike", 8.4, 5.2,
                "Unusual surge in power usage, possibly due to AC load.", "High"));
        anomalies.add(new Anomaly("22:00", "Mild Deviation", 3.2, 2.8,
                "Slight increase in standby device consumption.", "Medium"));

        return anomalies;
    }

    @GetMapping("/report/pdf")
    public ResponseEntity<byte[]> generatePdfReport() throws Exception {
        ByteArrayOutputStream outputStream = new ByteArrayOutputStream();

        Document document = new Document();
        PdfWriter.getInstance(document, outputStream);
        document.open();

        document.add(new Paragraph("Energy Analytics Report", new Font(Font.FontFamily.HELVETICA, 18, Font.BOLD)));
        document.add(new Paragraph("Generated on: " + new java.util.Date().toString()));
        document.add(new Paragraph("\n"));

        document.add(new Paragraph("Summary:"));
        document.add(new Paragraph("• Total Consumption: 123.45 kW"));
        document.add(new Paragraph("• Total Generation: 98.76 kW"));
        document.add(new Paragraph("• Efficiency: 80.0%"));
        document.add(new Paragraph("• Trend: Decreasing"));
        document.add(new Paragraph("\nRecommendations:"));
        document.add(new Paragraph("1. Shift heavy loads to off-peak hours."));
        document.add(new Paragraph("2. Increase solar panel usage."));
        document.add(new Paragraph("3. Monitor anomaly alerts weekly."));
        document.add(new Paragraph("\nAnomalies:"));
        document.add(new Paragraph("• High spike at 17:00 (8.4 kW vs 5.2 kW)"));
        document.add(new Paragraph("• Mild deviation at 22:00 (3.2 kW vs 2.8 kW)"));

        document.close();

        byte[] pdfBytes = outputStream.toByteArray();

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_PDF);
        headers.setContentDispositionFormData("attachment", "energy-analytics-report.pdf");

        return new ResponseEntity<>(pdfBytes, headers, HttpStatus.OK);
    }
}
