//
//  ContentView.swift
//  BrainWaveApp
//
//  Created by Chandler Ketelsen on 7/12/25.
//

import SwiftUI

struct ContentView: View {
    var body: some View {
        AppCoordinator()
            .environmentObject(AppState())
    }
}

#Preview {
    ContentView()
}
