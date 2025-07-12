//
//  ParkingData.swift
//  BrainWaveApp
//
//  Created by Chandler Ketelsen on 7/12/25.
//

import Foundation

// MARK: - Parking Lot Data Models

struct ParkingLotData: Codable, Identifiable {
    let id: String
    let name: String
    let location: Location
    let capacity: Int
    let currentOccupancy: Int
    let timeSeriesData: [TimeSeriesPoint]
    let lastUpdated: Date
    
    var occupancyPercentage: Double {
        guard capacity > 0 else { return 0 }
        return Double(currentOccupancy) / Double(capacity) * 100
    }
    
    var availableSpaces: Int {
        return capacity - currentOccupancy
    }
}

struct Location: Codable {
    let latitude: Double
    let longitude: Double
    let address: String
}

struct TimeSeriesPoint: Codable, Identifiable {
    let id = UUID()
    let timestamp: Date
    let occupancy: Int
    let predictedOccupancy: Int?
    
    enum CodingKeys: String, CodingKey {
        case timestamp, occupancy, predictedOccupancy
    }
}

// MARK: - Mock Data Service

class ParkingDataService: ObservableObject {
    @Published var parkingLots: [ParkingLotData] = []
    @Published var isLoading = false
    @Published var error: String?
    
    func fetchParkingData() async {
        DispatchQueue.main.async {
            self.isLoading = true
            self.error = nil
        }
        
        // Simulate network delay
        try? await Task.sleep(nanoseconds: 1_000_000_000) // 1 second
        
        DispatchQueue.main.async {
            self.parkingLots = [ParkingLotData.mockData]
            self.isLoading = false
        }
    }
    
    func fetchParkingDataForTimeRange(startDate: Date, endDate: Date) async {
        await fetchParkingData()
    }
}

// MARK: - Mock Data for Development

extension ParkingLotData {
    static let mockData = ParkingLotData(
        id: "mock_lot_1",
        name: "Downtown Parking Garage",
        location: Location(
            latitude: 40.7128,
            longitude: -74.0060,
            address: "123 Main St, New York, NY"
        ),
        capacity: 72,
        currentOccupancy: 48,
        timeSeriesData: generateMockTimeSeriesData(),
        lastUpdated: Date()
    )
    
    private static func generateMockTimeSeriesData() -> [TimeSeriesPoint] {
        let calendar = Calendar.current
        let now = Date()
        var data: [TimeSeriesPoint] = []
        
        // Generate 24 hours of data (48 points, 30-minute intervals)
        for i in 0..<48 {
            let timestamp = calendar.date(byAdding: .minute, value: -i * 30, to: now) ?? now
            let baseOccupancy = 30
            let variation = Int.random(in: -10...15)
            let occupancy = max(0, min(72, baseOccupancy + variation))
            
            let predictedOccupancy = i < 24 ? max(0, min(72, occupancy + Int.random(in: -5...10))) : nil
            
            data.append(TimeSeriesPoint(
                timestamp: timestamp,
                occupancy: occupancy,
                predictedOccupancy: predictedOccupancy
            ))
        }
        
        return data.reversed()
    }
} 