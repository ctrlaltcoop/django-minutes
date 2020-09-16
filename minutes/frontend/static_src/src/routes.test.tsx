import React from "react";
import {expandPaths, idToRoute, RouteId} from "./routes";

const DummyComponent = () => <div/>

const testRoutePaths = {
  LEVEL_0_0: 'LEVEL_0_0',
  LEVEL_0_1: 'LEVEL_0_1',
  LEVEL_0_2: 'LEVEL_0_2',
  LEVEL_1_0: 'LEVEL_1_0',
  LEVEL_1_1: 'LEVEL_1_1',
  LEVEL_2_0: 'LEVEL_2_0',
  LEVEL_2_1: 'LEVEL_2_1',
}

const testRoutes = [{
  id: RouteId.HOME,
  path: testRoutePaths.LEVEL_0_0,
  component: DummyComponent,
},
  {
    id: RouteId.LOGIN,
    path: testRoutePaths.LEVEL_0_1,
    component: DummyComponent,
  },
  {
    id: RouteId.MEMBER_AREA,
    path: testRoutePaths.LEVEL_0_2,
    component: DummyComponent,
    routes: [
      {
        id: RouteId.MEETING_SERIES,
        path: testRoutePaths.LEVEL_1_0,
        component: DummyComponent,
      },
      {
        id: RouteId.ADMIN,
        path: testRoutePaths.LEVEL_1_1,
        component: DummyComponent,
        routes: [
          {
            path: testRoutePaths.LEVEL_2_0,
            component: DummyComponent,
          },
          {
            id: RouteId.ADMIN_USERS,
            path: testRoutePaths.LEVEL_2_1,
            component: DummyComponent,
          }
        ]
      }
    ]
  },
];

describe('#expandPaths', () => {
  let expandedRoutes
  beforeEach(() => {
    expandedRoutes = expandPaths(testRoutes)
  })

  test('level 0 paths left the same', () => {
    expect(expandedRoutes[0].path).toEqual(testRoutePaths.LEVEL_0_0)
    expect(expandedRoutes[1].path).toEqual(testRoutePaths.LEVEL_0_1)
    expect(expandedRoutes[2].path).toEqual(testRoutePaths.LEVEL_0_2)
  })

  test('level 1 paths expanded', () => {
    expect(expandedRoutes[2].routes[0].path).toEqual(testRoutePaths.LEVEL_0_2 + testRoutePaths.LEVEL_1_0)
    expect(expandedRoutes[2].routes[1].path).toEqual(testRoutePaths.LEVEL_0_2 + testRoutePaths.LEVEL_1_1)
  })

  test('level 2 paths expanded', () => {
    expect(expandedRoutes[2].routes[1].routes[0].path).toEqual(
      testRoutePaths.LEVEL_0_2 + testRoutePaths.LEVEL_1_1 + testRoutePaths.LEVEL_2_0
    )
    expect(expandedRoutes[2].routes[1].routes[1].path).toEqual(
      testRoutePaths.LEVEL_0_2 + testRoutePaths.LEVEL_1_1 + testRoutePaths.LEVEL_2_1
    )
  })
})


describe('#idToRoute', () => {
  let expandedRoutes
  test('find home', () => {
    expect(idToRoute(RouteId.HOME, testRoutes)).toBeDefined()
    expect(idToRoute(RouteId.HOME, testRoutes)!!.path).toEqual(testRoutePaths.LEVEL_0_0)
  })

  test('find login', () => {
    expect(idToRoute(RouteId.LOGIN, testRoutes)).toBeDefined()
    expect(idToRoute(RouteId.LOGIN, testRoutes)!!.path).toEqual(testRoutePaths.LEVEL_0_1)
  })

  test('find member area', () => {
    expect(idToRoute(RouteId.MEMBER_AREA, testRoutes)).toBeDefined()
    expect(idToRoute(RouteId.MEMBER_AREA, testRoutes)!!.path).toEqual(testRoutePaths.LEVEL_0_2)
  })

  test('find meeting series', () => {
    expect(idToRoute(RouteId.MEETING_SERIES, testRoutes)).toBeDefined()
    expect(idToRoute(RouteId.MEETING_SERIES, testRoutes)!!.path).toEqual(testRoutePaths.LEVEL_1_0)
  })

  test('find admin', () => {
    expect(idToRoute(RouteId.ADMIN, testRoutes)).toBeDefined()
    expect(idToRoute(RouteId.ADMIN, testRoutes)!!.path).toEqual(testRoutePaths.LEVEL_1_1)
  })

  test('find home', () => {
    expect(idToRoute(RouteId.ADMIN_USERS, testRoutes)).toBeDefined()
    expect(idToRoute(RouteId.ADMIN_USERS, testRoutes)!!.path).toEqual(testRoutePaths.LEVEL_2_1)
  })

})
