import SwiftUI
import SceneKit

struct ParkingLot3DView: View {
    var body: some View {
        SceneView(
            scene: ParkingLot3DView.makeScene(),
            options: [.autoenablesDefaultLighting, .allowsCameraControl]
        )
        .edgesIgnoringSafeArea(.all)
    }
    
    static func makeScene() -> SCNScene {
        let scene = SCNScene()
        
        // Add a plane to represent the parking lot
        let lotWidth: CGFloat = 8
        let lotHeight: CGFloat = 5
        let lotPlane = SCNBox(width: lotWidth, height: 0.1, length: lotHeight, chamferRadius: 0)
        lotPlane.firstMaterial?.diffuse.contents = UIColor.darkGray
        let lotNode = SCNNode(geometry: lotPlane)
        lotNode.position = SCNVector3(0, -0.05, 0)
        scene.rootNode.addChildNode(lotNode)
        
        // Add parking space lines (2 rows of 4)
        addParkingLines(to: scene, rows: 2, cols: 4, lotWidth: lotWidth, lotHeight: lotHeight)
        
        // Add 5 cars in random spaces
        let occupiedSpaces = [(0,0), (0,1), (0,2), (1,0), (1,3)] // row, col
        addCars(to: scene, occupiedSpaces: occupiedSpaces, rows: 2, cols: 4, lotWidth: lotWidth, lotHeight: lotHeight)
        
        // Add a camera
        let cameraNode = SCNNode()
        cameraNode.camera = SCNCamera()
        cameraNode.position = SCNVector3(0, 7, 10)
        cameraNode.eulerAngles = SCNVector3(-Float.pi/5, 0, 0)
        scene.rootNode.addChildNode(cameraNode)
        
        return scene
    }
    
    static func addParkingLines(to scene: SCNScene, rows: Int, cols: Int, lotWidth: CGFloat, lotHeight: CGFloat) {
        let lineThickness: CGFloat = 0.05
        let spaceWidth = lotWidth / CGFloat(cols)
        let spaceHeight = lotHeight / CGFloat(rows)
        // Vertical lines
        for col in 1..<cols {
            let line = SCNBox(width: lineThickness, height: 0.11, length: lotHeight, chamferRadius: 0)
            line.firstMaterial?.diffuse.contents = UIColor.white
            let x = -lotWidth/2 + CGFloat(col) * spaceWidth
            let node = SCNNode(geometry: line)
            node.position = SCNVector3(x, 0.01, 0)
            scene.rootNode.addChildNode(node)
        }
        // Horizontal lines
        for row in 1..<rows {
            let line = SCNBox(width: lotWidth, height: 0.11, length: lineThickness, chamferRadius: 0)
            line.firstMaterial?.diffuse.contents = UIColor.white
            let z = -lotHeight/2 + CGFloat(row) * spaceHeight
            let node = SCNNode(geometry: line)
            node.position = SCNVector3(0, 0.01, z)
            scene.rootNode.addChildNode(node)
        }
        // Outer border
        let borderThickness: CGFloat = 0.08
        let borderColor = UIColor.white
        // Top
        let top = SCNBox(width: lotWidth, height: 0.12, length: borderThickness, chamferRadius: 0)
        top.firstMaterial?.diffuse.contents = borderColor
        let topNode = SCNNode(geometry: top)
        topNode.position = SCNVector3(0, 0.02, -lotHeight/2)
        scene.rootNode.addChildNode(topNode)
        // Bottom
        let bottom = SCNBox(width: lotWidth, height: 0.12, length: borderThickness, chamferRadius: 0)
        bottom.firstMaterial?.diffuse.contents = borderColor
        let bottomNode = SCNNode(geometry: bottom)
        bottomNode.position = SCNVector3(0, 0.02, lotHeight/2)
        scene.rootNode.addChildNode(bottomNode)
        // Left
        let left = SCNBox(width: borderThickness, height: 0.12, length: lotHeight, chamferRadius: 0)
        left.firstMaterial?.diffuse.contents = borderColor
        let leftNode = SCNNode(geometry: left)
        leftNode.position = SCNVector3(-lotWidth/2, 0.02, 0)
        scene.rootNode.addChildNode(leftNode)
        // Right
        let right = SCNBox(width: borderThickness, height: 0.12, length: lotHeight, chamferRadius: 0)
        right.firstMaterial?.diffuse.contents = borderColor
        let rightNode = SCNNode(geometry: right)
        rightNode.position = SCNVector3(lotWidth/2, 0.02, 0)
        scene.rootNode.addChildNode(rightNode)
    }
    
    static func addCars(to scene: SCNScene, occupiedSpaces: [(Int, Int)], rows: Int, cols: Int, lotWidth: CGFloat, lotHeight: CGFloat) {
        let carWidth: CGFloat = lotWidth / CGFloat(cols) * 0.7
        let carHeight: CGFloat = 0.5
        let carLength: CGFloat = lotHeight / CGFloat(rows) * 0.8
        let spaceWidth = lotWidth / CGFloat(cols)
        let spaceHeight = lotHeight / CGFloat(rows)
        let carColors: [UIColor] = [.blue, .red, .green, .yellow, .orange]
        for (i, (row, col)) in occupiedSpaces.enumerated() {
            let car = SCNBox(width: carWidth, height: carHeight, length: carLength, chamferRadius: 0.1)
            car.firstMaterial?.diffuse.contents = carColors[i % carColors.count]
            let carNode = SCNNode(geometry: car)
            let x = -lotWidth/2 + spaceWidth * (CGFloat(col) + 0.5)
            let z = -lotHeight/2 + spaceHeight * (CGFloat(row) + 0.5)
            carNode.position = SCNVector3(x, CGFloat(Float(carHeight/2 + 0.05)), z)
            scene.rootNode.addChildNode(carNode)
        }
    }
}

struct ParkingLot3DView_Previews: PreviewProvider {
    static var previews: some View {
        ParkingLot3DView()
    }
} 
