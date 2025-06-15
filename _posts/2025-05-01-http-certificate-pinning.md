---
layout: blog-post
title: "HTTP Certificate Pinning"
excerpt: "HTTP Certificate Pinning"
disqus_id: /2025/05/01/http-certificate-pinning/
tags:
    - Security
---

Certificate pinning code for Java

```java
package org.example;

import javax.net.ssl.*;
import java.io.*;
import java.net.URL;
import java.security.MessageDigest;
import java.security.cert.Certificate;
import java.security.cert.X509Certificate;
import java.util.Base64;

public class CertificatePinningClient {

    // SHA-256 fingerprint of the expected certificate
    // You need to replace this with the actual certificate fingerprint of madhur.co.in
    private static final String EXPECTED_CERT_SHA256 = "YOUR_CERT_FINGERPRINT_HERE";

    public static void main(String[] args) {
        try {
            String fingerprint = getCertificateFingerprint("https://localhost:8443");
            System.out.println(fingerprint);
          //  String response = makeSecureRequest("https://madhur.co.in");
           // System.out.println("Response: " + response);
        } catch (Exception e) {
            System.err.println("Error: " + e.getMessage());
            e.printStackTrace();
        }
    }

    public static String makeSecureRequest(String urlString) throws Exception {
        URL url = new URL(urlString);
        HttpsURLConnection connection = (HttpsURLConnection) url.openConnection();

        // Set up custom SSL context with certificate pinning
        SSLContext sslContext = SSLContext.getInstance("TLS");
        sslContext.init(null, new TrustManager[]{new PinningTrustManager()}, null);
        connection.setSSLSocketFactory(sslContext.getSocketFactory());

        // Set request properties
        connection.setRequestMethod("GET");
        connection.setConnectTimeout(10000);
        connection.setReadTimeout(10000);

        // Make the request
        connection.getResponseCode();

        // Read the response
        StringBuilder response = new StringBuilder();
        try (BufferedReader reader = new BufferedReader(
                new InputStreamReader(connection.getInputStream()))) {
            String line;
            while ((line = reader.readLine()) != null) {
                response.append(line).append("\n");
            }
        }

        connection.disconnect();
        return response.toString();
    }

    // Custom TrustManager that implements certificate pinning
    private static class PinningTrustManager implements X509TrustManager {

        @Override
        public void checkClientTrusted(X509Certificate[] chain, String authType) {
            // Not used for client certificates in this example
        }

        @Override
        public void checkServerTrusted(X509Certificate[] chain, String authType)
                throws java.security.cert.CertificateException {

            if (chain == null || chain.length == 0) {
                throw new java.security.cert.CertificateException("Certificate chain is empty");
            }

            // Get the server certificate (first in chain)
            X509Certificate serverCert = chain[0];

            try {
                // Calculate SHA-256 fingerprint of the certificate
                MessageDigest md = MessageDigest.getInstance("SHA-256");
                byte[] certBytes = serverCert.getEncoded();
                byte[] fingerprint = md.digest(certBytes);
                String certFingerprint = Base64.getEncoder().encodeToString(fingerprint);

                System.out.println("Server certificate fingerprint: " + certFingerprint);
                System.out.println("Expected fingerprint: " + EXPECTED_CERT_SHA256);

                // Check if the certificate matches our pinned certificate
                if (!EXPECTED_CERT_SHA256.equals(certFingerprint)) {
                    throw new java.security.cert.CertificateException("Certificate pinning failed! " +
                            "Expected: " + EXPECTED_CERT_SHA256 +
                            ", Got: " + certFingerprint);
                }

                System.out.println("Certificate pinning validation passed!");

            } catch (Exception e) {
                throw new java.security.cert.CertificateException("Error validating certificate: " + e.getMessage(), e);
            }
        }

        @Override
        public X509Certificate[] getAcceptedIssuers() {
            return new X509Certificate[0];
        }
    }

    // Utility method to get certificate fingerprint for a given URL
    // Run this first to get the actual certificate fingerprint
    public static String getCertificateFingerprint(String urlString) throws Exception {
        URL url = new URL(urlString);
        HttpsURLConnection connection = (HttpsURLConnection) url.openConnection();
        connection.connect();

        Certificate[] certificates = connection.getServerCertificates();
        if (certificates.length > 0) {
            X509Certificate cert = (X509Certificate) certificates[0];
            MessageDigest md = MessageDigest.getInstance("SHA-256");
            byte[] fingerprint = md.digest(cert.getEncoded());
            return Base64.getEncoder().encodeToString(fingerprint);
        }

        connection.disconnect();
        throw new Exception("No certificates found");
    }


}

```