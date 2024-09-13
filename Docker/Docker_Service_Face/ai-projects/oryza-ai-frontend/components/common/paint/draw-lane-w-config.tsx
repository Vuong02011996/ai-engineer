import React, { useRef, useState, useEffect } from "react";
import { DrawLaneToolbar, IDrawLaneToolbarRef } from "./toolbar/draw-lane-toolbar";
import { ChooseLaneVehicleMultiple } from "../../dialog/config-ai-lane-violation/choose-lane-vehicle";

interface Point {
  x: number;
  y: number;
  laneIndex?: number;
}

export interface IDrawLaneWithConfigProps {
  image: string;
  onReloadImage: () => void;
  onSubmit: (lanes: string, codes: string) => void;
  lanes_str: string;
  codes_str: string;
}

export const DrawLaneWithConfig = (props: IDrawLaneWithConfigProps) => {
  const canvasRef = useRef<any>(null);
  const boxRef = useRef<HTMLDivElement | null>(null);
  const [points, setPoints] = useState<Point[]>([]);
  const [tempPoints, setTempPoints] = useState<Point[]>([]);
  const [dragging, setDragging] = useState(false);
  const [dragIndex, setDragIndex] = useState<any>(null);
  const [draggingShape, setDraggingShape] = useState(false);
  const [image, setImage] = useState<any>(null);
  const [isPen, setIsPen] = useState(true);
  const [isDrawingLane, setIsDrawingLane] = useState(false);
  const [lanes, setLanes] = useState<any[]>([]);
  const toolbarRef = useRef<IDrawLaneToolbarRef>(null);
  const [laneIndex, setLaneIndex] = useState(-1);
  const [isRemovingLane, setIsRemovingLane] = useState(false);
  const [laneVehicles, setLaneVehicles] = useState<{ [key: number]: { item: any; checked: boolean; laneIndex: number }[] }>({});

  const drawCurrentLanes = () => {
    const canvas = canvasRef.current;
    console.log('Lane now', lanes)
    const context = canvasRef.current.getContext("2d");
    context.clearRect(0, 0, canvasRef.current.width, canvasRef.current.height);
    if (image) {
      context.drawImage(image, 0, 0, canvas.width, canvas.height);
    }
    for (let lane of lanes) {
      const points = lane.points;
      context.beginPath();
      context.moveTo(points[0].x, points[0].y);
      context.lineTo(points[1].x, points[1].y);
      context.lineTo(points[2].x, points[2].y);
      context.lineTo(points[3].x, points[3].y);
      context.lineTo(points[0].x, points[0].y);
      context.strokeStyle = "#78C6E7";
      context.lineWidth = 5;
      context.fillStyle = "rgba(241, 46, 233, 0.50)";
      context.fill();
      // set the index of the lane
      context.font = "30px Arial";
      context.fillStyle = "red";
      const centerPoint = {
        x: (points[0].x + points[1].x) / 2,
        y: (points[0].y + points[1].y) / 2,
      };
      context.fillText(`${lane.index}`, centerPoint.x, centerPoint.y);

      // draw lane vector
      drawArrow(points);
    }
  };

  useEffect(() => {
    console.log('UseEffect to DrawLane, Current lanes', lanes)
    drawCurrentLanes();
    // update lane vehicles
    // const indexAvailable = lanes.map((lane) => lane.index);
    // console.log('indexAvailable', indexAvailable)
    // // keep those lane vehicles that are still available
    // for (const lv in laneVehicles) {
    //   if (!(lv in indexAvailable)) {
    //     console.log('remove', laneVehicles[lv])
    //     delete laneVehicles[lv];
    //   }
    // }
    // setLaneVehicles(laneVehicles);
  }, [lanes]);

  useEffect(() => {
    const canvas = canvasRef.current;
    const context = canvas.getContext("2d");
    context.clearRect(0, 0, canvas.width, canvas.height);

    if (image) {
      context.drawImage(image, 0, 0, canvas.width, canvas.height);
    }

    drawCurrentLanes();

    if (tempPoints.length >= 2) {
      context.beginPath();
      context.moveTo(tempPoints[0].x, tempPoints[0].y);
      for (let i = 1; i < tempPoints.length; i++) {
        context.lineTo(tempPoints[i].x, tempPoints[i].y);
        if (tempPoints.length == 4) {
          context.lineTo(tempPoints[0].x, tempPoints[0].y);
          // new lane added
          // console.log('current lane index', laneIndex)
          // console.log('current temp points', tempPoints) 
          // draw lane vector
          drawArrow(tempPoints);
  
          // done drawing lane
          setIsDrawingLane(false);
          
          // change toolbar to NONE
          if (toolbarRef.current) {
            // console.log("Toolbar set to NONE");
            toolbarRef.current.setToolbar("NONE");
  
            // update lanes
            handleUpdateLanes();
          }
        }
      }
      context.strokeStyle = "#78C6E7";
      context.lineWidth = 5;
      context.stroke();
    }

    // Draw the points for visual feedback
    tempPoints.forEach((tempPoint, index) => {
      context.beginPath();
      context.arc(tempPoint.x, tempPoint.y, 5, 0, 2 * Math.PI);
      context.fillStyle = dragIndex === index ? "red" : "#007DC0";
      context.fill();
    });
    // submitLane();
  }, [tempPoints, image, dragIndex]);

  const handleUpdateLanes = () => {
    // commit tempPoints to lanes
    // set lane vehicles
    const newLane = {
      points: tempPoints,
      index: laneIndex,
    };
    
    setLanes([...lanes, newLane]);
    setTempPoints([]);
  };

  const handleCanvasClick = (event: any) => {
    if (draggingShape) {
      setdrag(true);
      const rect = canvasRef.current.getBoundingClientRect();
      const x = event.clientX - rect.left;
      const y = event.clientY - rect.top;
      setOffset({ x, y, laneIndex });
      return;
    }
    if (!image) return;

    const rect = canvasRef.current.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;

    // Draw lane
    if (isDrawingLane) {
      // Check if clicking near an existing point to start dragging
      for (let i = 0; i < tempPoints.length; i++) {
        const tempPoint = tempPoints[i];
        if (Math.abs(tempPoint.x - x) < 10 && Math.abs(tempPoint.y - y) < 10) {
          setDragIndex(i);
          setDragging(true);
          return;
        }
      }
      const newTempPoints = [...tempPoints, { x, y, laneIndex }];
      setTempPoints(newTempPoints);
      setDragIndex(newTempPoints.length - 1);
    }
    else if (isRemovingLane) {
      const clickedPoint = { x, y, laneIndex };
      // console.log('Clicked Point:', clickedPoint);
  
      setLanes((prevLanes) => {
        // console.log('Previous Lanes:', prevLanes);

        const updatedLanes = prevLanes.filter((lane) => {
            // console.log('Checking Lane:', lane);

            const isInsideLane = isPointInPolygon(clickedPoint, lane.points);
            // console.log('Is Inside Lane:', isInsideLane);
            return !isInsideLane;
        });

        // console.log('Updated Lanes:', updatedLanes);
        return updatedLanes;
      });
    }
  };

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

  const drawArrow = (points: Point[]) => {
    const midPoints = [
      { x: (points[0].x + points[3].x) / 2, y: (points[0].y + points[3].y) / 2 },
      { x: (points[1].x + points[2].x) / 2, y: (points[1].y + points[2].y) / 2 },
    ];
    const context = canvasRef.current.getContext("2d");
    context.beginPath();
    context.moveTo(midPoints[0].x, midPoints[0].y);
    context.lineTo(midPoints[1].x, midPoints[1].y);
    context.strokeStyle = "#78C6E7";
    context.lineWidth = 3;
    context.stroke();

    // arrowhead
    const headlen = 10; // length of head in pixels
    const angle = Math.atan2(midPoints[1].y - midPoints[0].y, midPoints[1].x - midPoints[0].x);
    context.beginPath();
    context.moveTo(midPoints[1].x, midPoints[1].y);
    context.lineTo(
      midPoints[1].x - headlen * Math.cos(angle - Math.PI / 6),
      midPoints[1].y - headlen * Math.sin(angle - Math.PI / 6)
    );
    context.lineTo(
      midPoints[1].x - headlen * Math.cos(angle + Math.PI / 6),
      midPoints[1].y - headlen * Math.sin(angle + Math.PI / 6)
    );
    context.lineTo(midPoints[1].x, midPoints[1].y);
    context.lineTo(
      midPoints[1].x - headlen * Math.cos(angle - Math.PI / 6),
      midPoints[1].y - headlen * Math.sin(angle - Math.PI / 6)
    );
    context.strokeStyle = "#FFF68F";
    context.lineWidth = 5;
    context.stroke();
    return context;
  };


  const handleMouseMove = (event: any) => {
    if (draggingShape && drag) {
      const rect = canvasRef.current.getBoundingClientRect();
      const x = event.clientX - rect.left;
      const y = event.clientY - rect.top;

      const dx = x - offset.x;
      const dy = y - offset.y;

      setPoints(points.map((point) => ({ x: point.x + dx, y: point.y + dy, laneIndex: point.laneIndex })));
      // handleSubmit(
      //   points.map((point) => ({ x: point.x + dx, y: point.y + dy, laneIndex: point.laneIndex }))
      // );

      setOffset({ x, y });
      return;
    }

    if (!dragging) return;

    const rect = canvasRef.current.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;
    const laneIndex = points[dragIndex].laneIndex;
    const newPoints = [...points];
    newPoints[dragIndex] = { x, y, laneIndex };
    setPoints(newPoints);
    // console.log('point', newPoints)
    // handleSubmit(newPoints);
  };

  const handleMouseUp = () => {
    if (draggingShape) {
      setdrag(false);
      return;
    }
    setDragging(false);
  };

  // this load the image and settings
  const handleImageUpload = (event: any) => {
    if (event) {
      const file = event.target.files[0];
      if (!file) return;
      const img = new Image();
      img.onload = () => {
        setImage(img);
        const canvas = canvasRef.current;

        const MAX_WIDTH = boxRef.current?.clientWidth || 500;
        const ratio = img.width / img.height;

        const width = img.width > MAX_WIDTH ? MAX_WIDTH : img.width;
        const height = img.width > MAX_WIDTH ? MAX_WIDTH / ratio : img.height;
        canvas.width = width;
        canvas.height = height;
      };
      img.src = URL.createObjectURL(file);
    } else {
      const img = new Image();
      img.onload = () => {
        setImage(img);
        const canvas = canvasRef.current;

        const MAX_WIDTH = boxRef.current?.clientWidth || 500;
        const ratio = img.width / img.height;

        const width = img.width > MAX_WIDTH ? MAX_WIDTH : img.width;
        const height = img.width > MAX_WIDTH ? MAX_WIDTH / ratio : img.height;

        canvas.width = width;
        canvas.height = height;

        if (props.lanes_str) {
          // Decode lanes
          console.log('Lanes from db', props.lanes_str)
          console.log('Set on canvas...')
          try {
            const lanes = JSON.parse(props.lanes_str);
            // console.log('Lanes:', lanes);
            let existed_lanes = [];
            let idx = -1;
            for (const key in lanes) {
              idx += 1;
              const lane = lanes[key];
              let existed_points = [];
              for (const key in lane) {
                const point = lane[key];
                existed_points.push(
                  { x: point[0] * width, y: point[1] * height, laneIndex: idx },
                );
              }
              existed_lanes.push({
                points: existed_points,
                index: idx
              });
            }
            console.log('Set lanes:', existed_lanes);
            setLanes(existed_lanes);
            console.log('Set lane index:', idx);
            setLaneIndex(idx);
          } catch (error) {
            console.error('Failed to parse lanes:', error);
            console.log('Received lanes:', props.lanes_str);
          }
        }
        if (props.codes_str) {
          // Decode codes
          console.log('Codes from db', props.codes_str)
          try {
            const codes = JSON.parse(props.codes_str);
            let laneVehicles: { [key: number]: { item: any; checked: boolean; laneIndex: number; }[] } = {};
            
            for (const key in codes) {
              const lane_code = codes[key];
              let laneVehicle: { item: any; checked: boolean; laneIndex: number; }[] = [];
              
              for (const subKey in lane_code) {
                const code = lane_code[subKey];
                laneVehicle.push({ item: code, checked: true, laneIndex: Number(subKey) });
              }
              
              laneVehicles[Number(key)] = laneVehicle;
            }
            
            setLaneVehicles(laneVehicles);
          } catch (error) {
            console.error('Failed to parse codes:', error);
            console.log('Received codes:', props.codes_str);
          }
        }
      }

      img.src = props.image ?? "/images/img-mock.jpg";
    }
  };

  useEffect(() => {
    handleImageUpload(null);
  }, [props.image]);


  const [offset, setOffset] = useState<any>({ x: 0, y: 0 });
  const [drag, setdrag] = useState(false);

  // * * * * * * * * * * * * * * * * *
  const handleSubmit = () => {
    if (!image) return;
    const MAX_WIDTH = boxRef.current?.clientWidth || 500;
    const ratio = image.width / image.height;
    const width = image.width > MAX_WIDTH ? MAX_WIDTH : image.width;
    const height = image.width > MAX_WIDTH ? MAX_WIDTH / ratio : image.height;

    // encode lane
    let lanes_ = []; 
    for (const key in lanes) {
      const lane = lanes[key].points;
      let lane_ = [];
      for (const key1 in lane) {
        const point = lane[key1];
        const x = point.x / width;
        const y = point.y / height;
        lane_.push([x, y]);
      }
      lanes_.push(lane_);
    }
    const lane_submit = JSON.stringify(lanes_);
    console.log('Ready to submit lane', lane_submit)
    // encode lane vehicles
    let codes = [];
    for (const key in lanes) {
      const laneIndex = lanes[key].index;
      // get lane vehicles
      const laneVehicle = laneVehicles[laneIndex];
      let code = "";
      for (const key in laneVehicle)
        if (laneVehicle[key].checked) {
          code += laneVehicle[key].item.toString();
        }
      codes.push(code);
    }
    const code_submit = JSON.stringify(codes);
    console.log('Ready to submit vehicle codes', code_submit)  
    props.onSubmit(lane_submit, code_submit);
  };

  const updateLaneVehicle = (laneIndex: number, value: { item: any; checked: boolean; laneIndex: number }[]) => {
    setLaneVehicles((prev) => ({
      ...prev,
      [laneIndex]: value,
    }));
  };

  // when lane vehicles change, print out
  useEffect(() => {
    console.log('Lane Vehicles changed', laneVehicles)
    handleSubmit();
  }, [laneVehicles]);

  return (
    <div style={{ height: '540px'}}>
      <div className="relative">
        <DrawLaneToolbar
          ref={toolbarRef}
          onAddLane={() => {
            setLaneIndex(laneIndex + 1);
            setIsDrawingLane(true);
            setDraggingShape(false);
            setIsRemovingLane(false);
          }}
          onMove={() => {
            setDraggingShape(!draggingShape);
            setIsPen(false);
          }}
          // onRemoveLane={() => {}}
          onRemoveLane={() => {
            setIsRemovingLane(true);
            // setPoints((prev) => prev.filter((v, i) => i !== dragIndex));
            // setDragIndex(points.length - 2);
            // handleSubmit(points.filter((v, i) => i !== dragIndex));
          }}
          onReset={() => {
            setTempPoints([]);
            setLaneIndex(-1);
            setLanes([]);
            setLaneVehicles({});
            // handleSubmit([]);
          }}
          // isShowSubmit={points.length >= 3 && isPen}
          onSubmit={() => {
            handleSubmit();
            setIsDrawingLane(false);
          }}
          onRefresh={props.onReloadImage}
        />
        <div ref={boxRef} style={{ height: '100%', overflow: 'auto' }}>
          <canvas
            ref={canvasRef}
            onMouseMove={handleMouseMove}
            onMouseDown={handleCanvasClick}
            onMouseUp={handleMouseUp}
            style={{ display: 'block', width: '100%', height: 'auto' }}
          />
        </div>
    </div>
      {lanes.length > 0 && lanes.map((lane) => (
        <div key={lane.index}>
          <ChooseLaneVehicleMultiple
            laneIndex={lane.index}
            value={laneVehicles[lane.index] || []}
            onChange={(value) => {
              updateLaneVehicle(lane.index, value);
            }}
          />
        </div>
      ))}
    </div>
  );
};
