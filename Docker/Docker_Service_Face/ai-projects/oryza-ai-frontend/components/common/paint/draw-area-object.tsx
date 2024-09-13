import React, { useRef, useState, useEffect } from "react";
import { DrawAreaObjectToolbar } from "@/components/common/paint/toolbar/draw-area-object-toolbar";
interface Point {
  x: number;
  y: number;
}

export interface IPainComponentsProps {
  image: string;
  onReloadImage: () => void;
  onSubmit: (area: string, object: string) => void;
  area_str: string;
  object_str: string;
}

export const DrawAreaObjectsConfig = (props: IPainComponentsProps) => {
  const canvasRef = useRef<any>(null);
  const boxRef = useRef<HTMLDivElement | null>(null);

  const [points, setPoints] = useState<Point[]>([]);
  const [objectPoints, setObjectPoints] = useState<Point[]>([]);

  const [dragging, setDragging] = useState(false);
  const [draggingShape, setDraggingShape] = useState(false);

  const [dragIndex, setDragIndex] = useState<any>(null);
  const [dragObjectIndex, setObjectDragIndex] = useState<any>(null);

  const [image, setImage] = useState<any>(null);

  const [drawingArea, setDrawingArea] = useState(false);
  const [drawingObjects, setDrawingObjects] = useState(false);

  const handleCanvasClick = (event: any) => {
    if (draggingShape) {
      setdrag(true);
      const rect = canvasRef.current.getBoundingClientRect();
      const x = event.clientX - rect.left;
      const y = event.clientY - rect.top;
      setOffset({ x, y });
      return;
    }
    if (!drawingArea && !drawingObjects) return;

    const rect = canvasRef.current.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;
    
    if (drawingArea) {
      // Check if clicking near an existing point to start dragging
      for (let i = 0; i < points.length; i++) {
        const point = points[i];
        if (Math.abs(point.x - x) < 10 && Math.abs(point.y - y) < 10) {
          setDragIndex(i);
          setDragging(true);
          return;
        }
      }
      const newPoints = [...points, { x, y }];
      setPoints(newPoints);
      setDragIndex(newPoints.length - 1);
    }
    else if ((drawingObjects)) {
      // Check if clicking near an existing point to start dragging
      for (let i = 0; i < objectPoints.length; i++) {
        const point = objectPoints[i];
        if (Math.abs(point.x - x) < 5 && Math.abs(point.y - y) < 5) {
          setObjectDragIndex(i);
          setDragging(true);
          return;
        }
      }
      if (objectPoints.length >= 2) {
        return;
      }
      const newObjectPoints = [...objectPoints, { x, y }];
      setObjectPoints(newObjectPoints);
      setObjectDragIndex(newObjectPoints.length - 1);
    }
  };

  // Check if a point is inside a polygon
  const isPointInPolygon = (point: Point, polygon: Point[]) => {
    let isInside = false;
    const { x, y } = point;
    for (let i = 0, j = polygon.length - 1; i < polygon.length; j = i++) {
      const xi = polygon[i].x, yi = polygon[i].y;
      const xj = polygon[j].x, yj = polygon[j].y;
  
      const intersect = ((yi > y) !== (yj > y)) &&
                        (x < (xj - xi) * (y - yi) / (yj - yi) + xi);
      if (intersect) isInside = !isInside;
    }
    return isInside;
  };

  const isPointInRectangle = (point: Point, rectPoints: Point[]) => {
    const [p1, p2] = rectPoints;
    const minX = Math.min(p1.x, p2.x);
    const maxX = Math.max(p1.x, p2.x);
    const minY = Math.min(p1.y, p2.y);
    const maxY = Math.max(p1.y, p2.y);
  
    return point.x >= minX && point.x <= maxX && point.y >= minY && point.y <= maxY;
  };

  const handleMouseMove = (event: any) => {
    // if dragging shape, move the shape
    // else move the point
    if (draggingShape && drag) {
      const rect = canvasRef.current.getBoundingClientRect();
      const x = event.clientX - rect.left;
      const y = event.clientY - rect.top;

      const dx = x - offset.x;
      const dy = y - offset.y;

      const clickedPoint = { x, y };

      // Check if the clicked point is inside the area of points
      const isInsidePoints = isPointInPolygon(clickedPoint, points);
      // Check if the clicked point is inside the rectangle defined by objectPoints
      const isInsideObjectPoints = isPointInRectangle(clickedPoint, objectPoints);

      if (isInsidePoints && !isInsideObjectPoints) {
        // Move points
        setPoints(points.map((point) => ({ x: point.x + dx, y: point.y + dy })));
      } else if (isInsideObjectPoints) {
        // Move objectPoints
        setObjectPoints(objectPoints.map((point) => ({ x: point.x + dx, y: point.y + dy })));
      }
      setOffset({ x, y });
      return;
    }

    if (!dragging) return;

    const rect = canvasRef.current.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;
    if (drawingArea) {
      const newPoints = [...points];
      newPoints[dragIndex] = { x, y };
      setPoints(newPoints);
    } else if (drawingObjects) {
      const newPoints = [...objectPoints];
      newPoints[dragObjectIndex] = { x, y };
      setObjectPoints(newPoints);
    }
  };

  const handleMouseUp = () => {
    // when the left mouse button is released, stop dragging
    if (draggingShape) {
      console.log("up");
      setdrag(false);
      return;
    }
    setDragging(false);
    // setDragIndex(null);
  };

  function convertPoint(pointArr: any, width: any, height: any) {
    if (pointArr) {
      let result: any = [];
      const points = JSON.parse(pointArr);

      for (const key in points) {
        const element = {
          x: points[key][0] * width,
          y: points[key][1] * height,
        };
        result.push(element);
      }
      return result;
    }

    return [];
  }

  const handleImageUpload = (event: any) => {
    if (event) {
      const file = event.target.files[0];
      if (!file) return;
      const img = new Image();
      img.onload = () => {
        setImage(img);
        const canvas = canvasRef.current;

        const MAX_WIDTH = boxRef.current?.clientWidth || 400;
        const ratio = img.width / img.height;

        const width = img.width > MAX_WIDTH ? MAX_WIDTH : img.width;
        const height = img.width > MAX_WIDTH ? MAX_WIDTH / ratio : img.height;

        // canvas.width = img.width;
        // canvas.height = img.height;
        canvas.width = width;
        canvas.height = height;
      };
      img.src = URL.createObjectURL(file);
    } else {
      const img = new Image();
      img.onload = () => {
        setImage(img);
        const canvas = canvasRef.current;

        const MAX_WIDTH = boxRef.current?.clientWidth || 400;
        const ratio = img.width / img.height;

        const width = img.width > MAX_WIDTH ? MAX_WIDTH : img.width;
        const height = img.width > MAX_WIDTH ? MAX_WIDTH / ratio : img.height;

        canvas.width = width;
        canvas.height = height;

        if (props.area_str) {
          try {
            const area = convertPoint(props.area_str, width, height);
            setPoints(area);
          } catch (error) {
            console.log(error);
          }
        }
        console.log("Leaving Draw: point loaded", points);
        if (props.object_str) {
          try {
            const object = convertPoint(props.object_str, width, height);
            setObjectPoints(object);
          } catch (error) {
            console.log(error);
          }
        }
        console.log("Leaving Draw: object loaded", objectPoints);
      };

      img.src = props.image ?? "/images/img-mock.jpg";
    }
  };

  useEffect(() => {
    handleImageUpload(null);
  }, [props.image]);

  // Draw the points for visual feedback
  useEffect(() => {
    const canvas = canvasRef.current;
    const context = canvas.getContext("2d");
    context.clearRect(0, 0, canvas.width, canvas.height);
  
    if (image) {
      context.drawImage(image, 0, 0, canvas.width, canvas.height);
    }
  
    // Draw points
    if (points.length > 1) {
      context.beginPath();
      context.moveTo(points[0].x, points[0].y);
      for (let i = 1; i < points.length; i++) {
        context.lineTo(points[i].x, points[i].y);
      }
      context.closePath();
      context.fillStyle = "rgba(241, 46, 233, 0.50)";
      context.fill();
  
      context.strokeStyle = "#78C6E7";
      context.lineWidth = 1;
      context.stroke();
    }
  
    points.forEach((point, index) => {
      context.beginPath();
      context.arc(point.x, point.y, 5, 0, 2 * Math.PI);
      context.fillStyle = dragIndex === index ? "red" : "#007DC0";
      context.fill();

        // Set the text style and print the index number next to the point
      context.fillStyle = "black"; // Set the text color
      context.font = "12px Arial"; // Set the text font and size
      context.fillText(index, point.x-3, point.y-3); // Print the index number next to the point
    });
  
    // Draw object points
    if (objectPoints.length >= 2) {
      context.beginPath();
      context.moveTo(objectPoints[0].x, objectPoints[0].y);
      context.lineTo(objectPoints[0].x, objectPoints[1].y);
      context.lineTo(objectPoints[1].x, objectPoints[1].y);
      context.lineTo(objectPoints[1].x, objectPoints[0].y);
      context.lineTo(objectPoints[0].x, objectPoints[0].y);
      context.closePath();
      context.fillStyle = "rgba(46, 241, 233, 0.50)";
      context.fill();
  
      context.strokeStyle = "#78C6E7";
      context.lineWidth = 1;
      context.stroke();
    }
    objectPoints.forEach((point, index) => {
      context.beginPath();
      context.arc(point.x, point.y, 5, 0, 2 * Math.PI);
      context.fillStyle = dragObjectIndex === index ? "red" : "#007DC0";
      context.fill();

          // Set the text style and print the index number next to the point
      context.fillStyle = "black"; // Set the text color
      context.font = "12px Arial"; // Set the text font and size
      context.fillText(index, point.x-3, point.y-3); // Print the index number next to the point
    });
  
    // console.log("points", points);
    // console.log("objectPoints", objectPoints);
    handleSubmit();
  }, [points, objectPoints, image, dragIndex, dragObjectIndex]);

  const [offset, setOffset] = useState<any>({ x: 0, y: 0 });
  const [drag, setdrag] = useState(false);

  // * * * * * * * * * * * * * * * * *
  const handleSubmit = () => {
    if (!image) return;
    let area = [];
    let object = [];
    const MAX_WIDTH = boxRef.current?.clientWidth || 400;
    const ratio = image.width / image.height;

    const width = image.width > MAX_WIDTH ? MAX_WIDTH : image.width;
    const height = image.width > MAX_WIDTH ? MAX_WIDTH / ratio : image.height;

    for (const key in points) {
      const point = points[key];
      const x = point.x / width;
      const y = point.y / height;

      area.push([x, y]);
    }
    for (const key in objectPoints) {
      const point = objectPoints[key];
      const x = point.x / width;
      const y = point.y / height;

      object.push([x, y]);
    }
    console.log("Leaving Draw: Submit area", area);
    console.log("Leaving Draw: object", object);
    props.onSubmit(JSON.stringify(area), JSON.stringify(object));
  };

  return (
    <div>
      <div className="relative">
        <DrawAreaObjectToolbar
          onMove={() => {
            setDrawingArea(false);
            setDrawingObjects(false);
            setDraggingShape(true);
          }}
          onAddArea={() => {
            setDrawingArea(true);
            setDrawingObjects(false);
            setDraggingShape(false);
          }}
          onAddObjects={() => {
            setDrawingObjects(true);
            setDrawingArea(false);
            setDraggingShape(false);
          }}
          onRemove={() => {
            if (drawingArea) {
              setPoints((prev) => prev.filter((v, i) => i !== dragIndex));
              setDragIndex(points.length - 2);
            }
            if (drawingObjects) {
              setObjectPoints((prev) => prev.filter((v, i) => i !== dragObjectIndex));
              setObjectDragIndex(objectPoints.length - 2);
            }
          }}
          onReset={() => {
            setPoints([]);
            setDrawingArea(true);
            setDrawingObjects(false);
            setObjectPoints([]);
          }}
          onSubmit={() => {
            handleSubmit();
          }}
          onRefresh={props.onReloadImage}
        />
        <div ref={boxRef}>
          <canvas
            ref={canvasRef}
            onMouseMove={handleMouseMove}
            onMouseDown={handleCanvasClick}
            onMouseUp={handleMouseUp}
          />
        </div>
      </div>
    </div>
  );
};