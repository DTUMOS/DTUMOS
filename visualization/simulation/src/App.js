import 'mapbox-gl/dist/mapbox-gl.css';
import React, { useEffect, useState } from 'react';
import Slider from '@mui/material/Slider';
import axios from 'axios';
import Trip from './components/Trip';
import Report from './components/Report';
import Splash from './components/Splash';
import './css/app.css';

const getRestData = async (dataName) => {
  try {
    const res = await axios.get(`${process.env.PUBLIC_URL}/data/${dataName}.json`, {
      responseType: 'text'  // 텍스트로 받아서 처리
    });
    
    let data = res.data;
    
    // 문자열인 경우 NaN을 null로 치환 후 파싱
    if (typeof data === 'string') {
      console.log(`${dataName} 데이터 전처리 중...`);
      
      // NaN을 null로 치환 (JSON에서 유효한 값)
      data = data.replace(/\bNaN\b/g, 'null');
      
      try {
        return JSON.parse(data);
      } catch (parseError) {
        console.error(`${dataName} JSON 파싱 에러:`, parseError);
        console.log('문제가 되는 부분:', data.substring(0, 200));
        return null;
      }
    }
    
    return data;
  } catch (error) {
    console.error(`${dataName} 데이터 로드 실패:`, error);
    return null;
  }
};


const App = () => {
  const [timeRange, setTimeRange] = useState({ min: 0, max: 1440 });
  const [time, setTime] = useState(0); // 초기엔 0, 이후 useEffect에서 갱신됨
  const [data, setData] = useState({
    DRIVER_TRIP: [],
    DRIVER_MARKER: [],
    PASSENGER_MARKER: [],
    RESULT: [],
    check: [],
  });
  const [loaded, setLoaded] = useState(false);

  const minTime = timeRange.min;
  const maxTime = timeRange.max;
  const initTripData = 1;

  useEffect(() => {
    async function initSimulationSettings() {
      try {
        const res = await axios.get(`${process.env.PUBLIC_URL}/data/sim_config.json`);
        const cfg = res.data;
        setTimeRange({
          min: cfg.TIME_RANGE_START,
          max: cfg.TIME_RANGE_END
        });
        setTime(cfg.TIME_RANGE_START);
        console.log("시뮬 시간 범위 로드됨:", cfg.TIME_RANGE_START, "~", cfg.TIME_RANGE_END);
      } catch (err) {
        console.warn("sim_config.json 로드 실패, 기본값 사용");
        setTimeRange({ min: 1380, max: 1560 });
        setTime(1380);
      }
    }
    initSimulationSettings();
  }, []);
  // init
  useEffect(() => {
    async function getFetchData() {
      try {
        // 안전한 배열 생성
        const arrayLength = Math.max(0, Math.floor(Number(initTripData) || 0));
        console.log('Array length:', arrayLength);
        
        let startTimeArray = [];
        if (arrayLength > 0 && arrayLength < 10000) {
          startTimeArray = Array.from({ length: arrayLength }, (_, i) => i + minTime);
        }
        
        // 데이터 로드
        console.log('데이터 로딩 시작...');
        const DRIVER_TRIP = await getRestData('trip');
        const DRIVER_MARKER = await getRestData('vehicle_marker');
        const PASSENGER_MARKER = await getRestData('passenger_marker');
        const RESULT = await getRestData('result');
        
        // 로드된 데이터 확인
        console.log('DRIVER_TRIP:', DRIVER_TRIP ? `로드됨 (${Array.isArray(DRIVER_TRIP) ? DRIVER_TRIP.length + '개' : '배열 아님'})` : '실패');
        console.log('DRIVER_MARKER:', DRIVER_MARKER ? `로드됨 (${DRIVER_MARKER.length}개)` : '실패');
        console.log('PASSENGER_MARKER:', PASSENGER_MARKER ? `로드됨 (${PASSENGER_MARKER.length}개)` : '실패');
        console.log('RESULT:', RESULT ? `로드됨 (${RESULT.length}개)` : '실패');
        
        // 데이터 샘플 확인
        if (DRIVER_TRIP && Array.isArray(DRIVER_TRIP) && DRIVER_TRIP.length > 0) {
          console.log('DRIVER_TRIP 첫 번째 데이터:', DRIVER_TRIP[0]);
          
          // NaN이 null로 변환되었는지 확인
          const hasNull = DRIVER_TRIP.some(item => 
            item.trip && item.trip.some(coord => 
              coord.includes(null)
            )
          );
          if (hasNull) {
            console.warn('⚠️ 일부 좌표에 null 값이 있습니다. (원본 데이터의 NaN)');
          }
        }
        
        // 모든 데이터가 배열인지 확인
        const isValidData = 
          Array.isArray(DRIVER_TRIP) && 
          Array.isArray(DRIVER_MARKER) && 
          Array.isArray(PASSENGER_MARKER) && 
          Array.isArray(RESULT);
        
        if (isValidData) {
          setData({
            DRIVER_TRIP: DRIVER_TRIP,
            DRIVER_MARKER: DRIVER_MARKER,
            PASSENGER_MARKER: PASSENGER_MARKER,
            RESULT: RESULT,
            check: startTimeArray || []
          });
          setLoaded(true);
          console.log('모든 데이터 로드 완료!');
        } else {
          console.error('데이터 형식이 올바르지 않습니다.');
          // 부분적으로라도 로드 시도
          setData({
            DRIVER_TRIP: Array.isArray(DRIVER_TRIP) ? DRIVER_TRIP : [],
            DRIVER_MARKER: Array.isArray(DRIVER_MARKER) ? DRIVER_MARKER : [],
            PASSENGER_MARKER: Array.isArray(PASSENGER_MARKER) ? PASSENGER_MARKER : [],
            RESULT: Array.isArray(RESULT) ? RESULT : [],
            check: startTimeArray || []
          });
          setLoaded(true);
        }
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    }
    
    getFetchData();
  }, [minTime]);
  
  useEffect(() => {
    // 경고 방지를 위해 requestTime 변수 제거
    console.log("현재 요청 시간:", Math.floor(time) + initTripData);
  }, [time]);
  
  const SliderChange = value => {
    const time = value.target.value;
    setTime(time);
  };
  
  return (
    <div className='container'>
      {
        loaded ?
        <>
          <Trip
            data={data}
            minTime={minTime}
            maxTime={maxTime}
            time={time}
            setTime={setTime}
          >
          </Trip>
          <Slider id="slider" value={time} min={minTime} max={maxTime} onChange={SliderChange} track="inverted"/>
          <Report
            data={data}
            minTime={minTime}
            maxTime={maxTime}
            time={time}
            setTime={setTime}
          >
          </Report>
        </>
        :
        <Splash />
      }
    </div>
  );
};

export default App;