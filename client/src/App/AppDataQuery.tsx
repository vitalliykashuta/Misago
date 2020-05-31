import { useQuery } from "@apollo/react-hooks"
import { ApolloError } from "apollo-client"
import gql from "graphql-tag"
import React from "react"
import { ICategory, IForumStats, ISettings, IUser } from "../types"
import AppError from "./AppError"
import AppLoader from "./AppLoader"

const POLL_INTERVAL = 50 * 1000 // 50s

const INITIAL_DATA_QUERY = gql`
  fragment CategoryBanner on CategoryBanner {
    align
    background
    height
    url
  }

  fragment CategoryFields on Category {
    id
    name
    slug
    color
    icon
    banner {
      full {
        ...CategoryBanner
      }
      half {
        ...CategoryBanner
      }
    }
    threads
    posts
    isClosed
  }

  query InitialData {
    auth {
      id
      name
      slug
      avatars {
        size
        url
      }
      isAdministrator
      isModerator
    }
    categories {
      ...CategoryFields
      children {
        ...CategoryFields
      }
    }
    settings {
      bulkActionLimit
      forumIndexHeader
      forumIndexThreads
      forumIndexTitle
      forumName
      passwordMinLength
      passwordMaxLength
      usernameMinLength
      usernameMaxLength
    }
    forumStats {
      threads
      posts
      users
    }
  }
`

interface IInitialData {
  auth: IUser | null
  categories: Array<ICategory>
  settings: ISettings | null
  forumStats: IForumStats | null
}

interface IAppDataProps {
  children: (props: IAppDataChildrenProps) => React.ReactElement
}

interface IAppDataChildrenProps {
  data: IInitialData
  error: ApolloError | undefined
  loading: boolean
}

const defaultData = {
  auth: null,
  categories: [],
  settings: null,
  forumStats: null,
}

const AppDataQuery: React.FC<IAppDataProps> = ({ children }) => {
  const { data, error, loading } = useQuery<IInitialData>(INITIAL_DATA_QUERY, {
    pollInterval: POLL_INTERVAL,
  })

  if (!data) {
    if (loading) return <AppLoader />
    if (error) return <AppError />
  }

  return children({ error, loading, data: data || defaultData })
}

export default AppDataQuery