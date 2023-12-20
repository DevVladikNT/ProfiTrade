import { useState } from 'react'
import { Flex, Title } from '@tremor/react'

import './App.css'
import SearchBar from './components/SearchBar'
import PricePlot from './components/PricePlot'
import UserOperations from './components/UserOperations'

function App() {
  const [count, setCount] = useState(0);

  return (
    <>
      <h1>ProfiTrade</h1>
      <Flex flexDirection='col'>
        <SearchBar/>
        <Flex flexDirection='row'>
          <PricePlot/>
          <UserOperations/>
        </Flex>
      </Flex>
      
    </>
  );
}

export default App;
