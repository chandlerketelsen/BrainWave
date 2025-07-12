//
//  BrainWaveAppApp.swift
//  BrainWaveApp
//
//  Created by Chandler Ketelsen on 7/12/25.
//

import SwiftUI

@main
struct BrainWaveAppApp: App {
    @StateObject private var appState = AppState()
    
    var body: some Scene {
        WindowGroup {
            AppCoordinator()
                .environmentObject(appState)
        }
    }
}
