import Foundation
import Vision
import AppKit

guard CommandLine.arguments.count > 1 else {
    print("Usage: swift ocr.swift <image-path>")
    exit(1)
}

let imagePath = CommandLine.arguments[1]
let url = URL(fileURLWithPath: imagePath)

guard let image = NSImage(contentsOf: url),
      let tiffData = image.tiffRepresentation,
      let imageSource = CGImageSourceCreateWithData(tiffData as CFData, nil),
      let cgImage = CGImageSourceCreateImageAtIndex(imageSource, 0, nil) else {
    print("Failed to load image from \(imagePath)")
    exit(1)
}

let requestHandler = VNImageRequestHandler(cgImage: cgImage, options: [:])
let request = VNRecognizeTextRequest { request, error in
    if let error = error {
        print("Error: \(error)")
        return
    }
    guard let observations = request.results as? [VNRecognizedTextObservation] else { return }
    for observation in observations {
        if let candidate = observation.topCandidates(1).first {
            print(candidate.string)
        }
    }
}

request.recognitionLevel = .accurate
request.usesLanguageCorrection = true

do {
    try requestHandler.perform([request])
} catch {
    print("Error performing request: \(error)")
}
