interface Point {
  x: number;
  y: number;
}
export class Validator {
  static checkDifferent(input1: string, input2: string, name: string = "") {
    return (input1 === "" && input2 === "") || input1 !== input2 ? null : `${name} không được trùng nhau`;;
  }
  static checkNotChosen(input: string) {
    if (input === "") {
      return "Lựa chọn không hợp lệ";
    } else {
      return null;
    }
  }
  static checkNotEmpty(inputString: string, min?: number, max?: number) {
    if (typeof inputString === "string" && inputString.trim() === "") {
      return "Không được để trống";
    } else {
      if (min && inputString.length < min) {
        return `Quá ngắn`;
      }
      if (max && inputString.length > max) {
        return `Không được vượt quá ${max} ký tự`;
      }
      return null;
    }
  }
  static checkNumberString(inputString: string, min?: number, max?: number) {
    if (/^[0-9.e]+$/.test(inputString) || inputString === "") {
      return null;
    }
    return "Không đúng định dạng";
  }

  static checkLength(inputString: any, minLength: any) {
    if (typeof inputString === "string" && inputString.length < minLength) {
      // Nếu chiều dài của chuỗi nhỏ hơn độ dài tối thiểu
      return `Chuỗi phải có ít nhất ${minLength} ký tự.`;
    } else {
      // Nếu chiều dài của chuỗi đủ lớn
      return null;
    }
  }

  static checkPlaceNo(vehicleKey: string, value: string) {
    switch (vehicleKey) {
      case "XE_MAY_DIEN":
      case "XE_MAY":
      case "XE_O_TO":
        return Validator.checkNotEmpty(value);
      default:
        return null;
    }
  }

  static checkContainsOnlyNumbers(inputString: string) {
    // Sử dụng biểu thức chính quy để kiểm tra chuỗi chỉ chứa số
    const numbersRegex = /^[0-9]+$/;
    if (!numbersRegex.test(inputString)) {
      return "chỉ được nhập số";
    } else {
      return null;
    }
  }

  static checkValidEmail(email: string) {
    // Sử dụng biểu thức chính quy để kiểm tra địa chỉ email
    const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
    if (!emailRegex.test(email)) {
      return "Email không hợp lệ.";
    } else {
      return null;
    }
  }

  static checkValidPhoneNumber(phoneNumber: string) {
    // Sử dụng biểu thức chính quy để kiểm tra số điện thoại
    const phoneRegex = /^\d{10}$/; // Điều này kiểm tra xem số điện thoại có 10 chữ số hay không
    if (!phoneRegex.test(phoneNumber)) {
      return "Số điện thoại không hợp lệ.";
    } else {
      return null;
    }
  }

  static validateIPAddress(ipAddress: string) {
    const ipPattern =
      /^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;

    if (ipPattern.test(ipAddress)) {
      return null;
    } else {
      return "Địa chỉ IP không đúng định dạng";
    }
  }

  static validateRTSPUrl(url: string) {
    let inputString = url.trim();
    const rtsp_pool = ["rtsp", "http", "https"];
    for (let i = 0; i < rtsp_pool.length; i++) {
      if (inputString.startsWith(rtsp_pool[i])) {
        return null;
      } else {
        return "Rtsp không đúng định dạng";
      }
    }
  }
  static checkBoundary(input: string) {
    if (!input || input === "") {
      return "Bạn chưa vẽ ranh giới";
    }
    let boundary = JSON.parse(input);
    if (boundary.length <= 1) {
      return "Bạn chưa vẽ ranh giới";
    }

    return null;
  }

  

  // for leaving detection. now just handle for 1 area and 1 object
  static checkArea(area_str: string) {
    if (!area_str || area_str === "") {
      return "Bạn chưa vẽ khu vực theo dõi";
    }
    let area = JSON.parse(area_str);
    if (area.length <= 1) {
      return "Bạn chưa vẽ khu vực theo dõi";
    }

    // Check if the points form a convex polygon
    const isConvex = (points: Point[]) => {
      const crossProduct = (p1: Point, p2: Point, p3: Point) => {
        return (p2.x - p1.x) * (p3.y - p1.y) - (p2.y - p1.y) * (p3.x - p1.x);
      };

      let isPositive = null;
      for (let i = 0; i < points.length; i++) {
        const p1 = points[i];
        const p2 = points[(i + 1) % points.length];
        const p3 = points[(i + 2) % points.length];
        const cross = crossProduct(p1, p2, p3);
        if (cross !== 0) {
          if (isPositive === null) {
            isPositive = cross > 0;
          } else if (isPositive !== (cross > 0)) {
            return false;
          }
        }
      }
      return true;
    };

    if (!isConvex(area)) {
      return "Khu vực không hợp lệ";
    }

    return null;
  }

  // no need to check area_str, it is checked in checkBoundary
  static checkLeavingObjects(area_str: string, object_str: string) {
    const areaCheck = this.checkArea(area_str);
    console.log('area_check', areaCheck);

    if (areaCheck) {
      return areaCheck;
    }

    if (!object_str || object_str === "[]") {
      return "Bạn chưa vẽ đối tượng";
    }
    if (!area_str || area_str === "") {
      return 
    };

    let area_points = JSON.parse(area_str);
    let obj_points = JSON.parse(object_str);
    console.log('obj_points', obj_points);
    console.log('area_points', area_points);
    if (obj_points.length !== 2) {
      return "Đối tượng không hợp lệ";
    }
  
    const [rectPoint1, rectPoint2] = obj_points;
  
    // Calculate the other two corners of the rectangle
    const rectCorners = [
      rectPoint1,
      [rectPoint1[0], rectPoint2[1]],
      [rectPoint2[0], rectPoint1[1]],
      rectPoint2
    ];

    // Function to check if a point is inside a polygon
    const isPointInPolygon = (point: number[], polygon: number[][]) => {
      let isInside = false;
      for (let i = 0, j = polygon.length - 1; i < polygon.length; j = i++) {
        const xi = polygon[i][0], yi = polygon[i][1];
        const xj = polygon[j][0], yj = polygon[j][1];

        const intersect = ((yi > point[1]) !== (yj > point[1])) &&
                          (point[0] < (xj - xi) * (point[1] - yi) / (yj - yi) + xi);
        if (intersect) isInside = !isInside;
      }
      return isInside;
    };
  
    // Check if all corners of the rectangle are inside the polygon
    for (const corner of rectCorners) {
      if (!isPointInPolygon(corner, area_points)) {
        return "Đối tượng không nằm hoàn toàn trong khu vực theo dõi";
      }
    }
  
    return null;
  }

  static checkLine(input: string) {
    if (!input || input === "") {
      return "Bạn chưa vẽ ranh giới";
    }
    let line = JSON.parse(input);
    if (line.length <= 1) {
      return "Bạn chưa vẽ ranh giới";
    }
    return null;
  }

  // for lane violation detection
  static checkLanes(input: string) {
    if (!input || input === "") {
      return "Bạn chưa vẽ làn đường.";
    }
    return null;
  }

  static checkCodes(codes: any, lanes: string) {
    // vehicle code
    if (this.checkLanes(lanes)) {
      return "Bạn chưa vẽ làn đường.";
    }
    if (!codes || codes === "") {
      return "Bạn chưa chọn loại phương tiện.";
    }
    const lane_arr1 = JSON.parse(lanes).filter((lane: any) => lane !== null && lane !== '');
    const codes_arr1 = JSON.parse(codes).filter((code: any) => code !== null && code !== '');
    if (lane_arr1.length !== codes_arr1.length) {
      return "Bạn chưa chọn đủ loại phương tiện cho tất cả làn đường.";
    }
    return null;
  }

  // for line violation detection 
  static checkLines(input: string) {  
    if (!input || input === "") {
      return "Bạn chưa vẽ đường.";
    }
    return null;
  }

  static checkCoordinate(input: string) {
    input = input.replace(/\s+/g, ''); // Remove all whitespace
    // console.log('Sanitized input:', input); // Debugging log
    if (input === "") {
      return null;
    }
    const coordinateRegex = /^\d+\.\d+,\d+\.\d+$/;
    const isValid = coordinateRegex.test(input);
    // console.log('Is valid coordinate:', isValid); // Debugging log
    if (!isValid) {
      return "Tọa độ không đúng định dạng";
    } 
    return null;
  }
}
