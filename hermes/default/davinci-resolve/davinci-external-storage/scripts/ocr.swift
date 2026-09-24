import Vision
import AppKit
import Foundation

// Native macOS OCR via Apple Vision framework. Offline, no downloads.
// Build once: swiftc -o /tmp/ocr ocr.swift
// Usage: /tmp/ocr /path/to/screenshot.png
let args = CommandLine.arguments
guard args.count > 1 else { print("usage: ocr <image>"); exit(1) }
let path = args[1]
guard let img = NSImage(contentsOfFile: path),
      let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else {
    print("ERR: cannot load image"); exit(1)
}
let req = VNRecognizeTextRequest()
req.recognitionLevel = .accurate
req.usesLanguageCorrection = false
let handler = VNImageRequestHandler(cgImage: cg, options: [:])
try handler.perform([req])
for obs in (req.results ?? []) {
    print(obs.topCandidates(1).first?.string ?? "")
}
